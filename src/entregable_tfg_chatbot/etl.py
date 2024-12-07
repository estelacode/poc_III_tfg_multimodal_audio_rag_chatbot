import pandas as pd
import json
import shutil
import os

def load_csv(path: str) -> pd.DataFrame:
    
    """
    Load a CSV file into a pandas DataFrame.
    """
    df = pd.read_csv(path, sep=',')
    return df


def filter_rows(df: pd.DataFrame, condition: str) -> pd.DataFrame:
    """
    Filter rows in a DataFrame based on a condition.

    Parameters:
    df (pd.DataFrame): The DataFrame to filter.
    condition (str): The condition to filter rows by.

    Returns:
    pd.DataFrame: A DataFrame containing only the rows that match the condition.
    """
    return df.query(condition)


def select_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Select specific columns from a DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to select columns from.
    columns (list): A list of column names to select.

    Returns:
    pd.DataFrame: A DataFrame containing only the selected columns.
    """
    return df[columns]

def remove_incorrect_cataloged_rows(df: pd.DataFrame, index_rows: list) -> pd.DataFrame:
    """
    Remove rows from a DataFrame by their index.

    Parameters:
    df (pd.DataFrame): The DataFrame to remove rows from.
    index_rows (list): A list of row indices to remove.

    Returns:
    pd.DataFrame: A DataFrame with the specified rows removed.
    """
    for index in index_rows:
        df = df.drop(index, axis=0)
    return df.reset_index(drop=True)

def get_images_json_to_list(x:str) -> pd.DataFrame:
    
    """
    Converts a JSON string to a list.
    
    Parameters:
    x (str): The JSON string to convert.
    
    Returns:
    list: A list containing the elements from the JSON string.
    """
    json_cadena = x.replace("'", "\"")
    lista_imagenes = json.loads(json_cadena)
    return lista_imagenes

def get_one_image_of_list(df: pd.DataFrame, row_index: int, pattern_1:int, pattern_2:int) -> str:
    
    """
    Get one image of a list of images in a DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to modify.
    row_index (int): The row index for which to use the first pattern.
    pattern_1 (int): The first pattern to use.
    pattern_2 (int): The second pattern to use.

    Returns:
    pd.DataFrame: The modified DataFrame with an additional column 'iso_image'.
    """
    # Create empty columns
    df['iso_image'] = ''

    for index, row in df.iterrows():
        if index == row_index: 
            df.loc[index, 'iso_image'] = row['image_downloads'][pattern_1]
        else:
            df.loc[index, 'iso_image'] = row['image_downloads'][pattern_2]

    return df

def get_one_image_of_list_women(df: pd.DataFrame, pattern_1:int, pattern_2:int, pattern_3:int, pattern_4:int) -> pd.DataFrame:
    
    """
    Assigns a specific image from a list of images to a new column 'iso_image' in the DataFrame based on row indices.

    Parameters:
    df (pd.DataFrame): The DataFrame containing image lists in the 'image_downloads' column.
    pattern_1 (int): Index for selecting the image for certain rows.
    pattern_2 (int): Index for selecting the image for another set of rows.
    pattern_3 (int): Index for selecting the image for a specific row.
    pattern_4 (int): Index for selecting the image for all other rows.

    Returns:
    pd.DataFrame: The modified DataFrame with the 'iso_image' column populated.
    """
    df['iso_image'] = ''

    for index, row in df.iterrows():
        if index in  [39,44,97,154,187,247,252,269]:
            df.loc[index, 'iso_image'] = row['image_downloads'][pattern_1]
        elif index in [7,26,115,179,184,221,242,248,268]:
            df.loc[index, 'iso_image'] = row['image_downloads'][pattern_2]
        elif index in [235]:
            df.loc[index, 'iso_image'] = row['image_downloads'][pattern_3]
        else:
            df.loc[index, 'iso_image'] = row['image_downloads'][pattern_4]

    return df

def get_indices_images(df:pd.DataFrame,size:str, column:str='total_images'):
    
    """
    Get indices of rows in a DataFrame where a specified column matches a given size.

    Parameters:
    df (pd.DataFrame): The DataFrame to search for matching rows.
    size (str): The size to match in the specified column.
    column (str): The column to check for the matching size. Default is 'total_images'.

    Returns:
    list: A list of indices where the specified column matches the given size.
    """
    indice = df[df[column]==size].index.tolist()
    return indice

def preprocessing_woman_images(df: pd.DataFrame, indice_images: list, especial_indexes: list, x:int, y:int, w:int, z:int) -> pd.DataFrame:
    
    """
    Preprocess the images in a DataFrame by selecting a subset of images based on different criteria.

    Parameters:
    df (pd.DataFrame): The DataFrame to preprocess.
    indice_images (list): A list of indices where the preprocessing should be applied.
    especial_indexes (list): A list of indices where a special preprocessing should be applied.
    x (int): Index for selecting the subset of images for the special preprocessing.
    y (int): Index for selecting the subset of images for the special preprocessing.
    w (int): Index for selecting the subset of images for the regular preprocessing.
    z (int): Index for selecting the subset of images for the regular preprocessing.

    Returns:
    pd.DataFrame: The modified DataFrame with the 'image_downloads' column updated.
    """
    for i in indice_images:
        if i in especial_indexes:
            images_temp = df.loc[i, 'image_downloads'][x:y]
            df.at[i, 'image_downloads'] = images_temp
        else:
            images_temp = df.loc[i, 'image_downloads'][w:z]
            df.at[i, 'image_downloads'] = images_temp


def create_folder(path):
    
    """
    Create a new directory at the specified path.

    Parameters:
    path (str): The file path where the new directory should be created.

    Returns:
    None
    """
    return os.mkdir(path)


def copy_images_to_folder(df: pd.DataFrame, column:str, origin_image_path:str, destination_dir: str):
    
    """
    Copy images from a given origin directory to a destination directory based on a DataFrame column.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the column with image references.
    column (str): The column name in the DataFrame containing the image references.
    origin_image_path (str): The path to the origin directory containing the images.
    destination_dir (str): The path to the destination directory where the images will be copied.

    Returns:
    None
    """
    image_references = df[column].to_list()
    for reference in image_references:
        or_image_path = origin_image_path + reference + ".jpg"
        shutil.copy2(or_image_path, destination_dir)


def create_txt_files(df: pd.DataFrame, txt_dir: str):
    
    """
    Create a new text file for each image reference in the given DataFrame, containing some product information.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the column with image references and other columns with product information.
    txt_dir (str): The path to the directory where the text files will be created.

    Returns:
    None
    """
    
    for row in df.iterrows():
        name = str(row[1]['name']) + '.'
        #name = 'Name: ' + str(row[1]['name']) + '\n'
        descripcion = str(row[1]['description']) + '.'
        #descripcion = 'Description: ' + str(row[1]['description']) + '\n'
        price = 'Price: ' + str(row[1]['price']) 
        #currency = 'Currency: ' + str(row[1]['currency']) 
        images_reference = row[1]['iso_image']
        with open(txt_dir + images_reference + '.txt', 'w', encoding='utf-8') as f:
            f.write(name) 
            f.write(descripcion)
            f.write(price)
            #f.write(currency)


def etl_women(csv_path:str, origin_images_path:str, txt_image_dir:str, csv_final_path:str):

    """
    Perform an ETL process on a CSV file containing women's shoe data, preprocess images, and generate output files.

    Parameters:
    csv_path (str): The file path to the input CSV file.
    origin_images_path (str): The directory path containing the original images.
    txt_dir (str): The directory path where text files will be created.
    image_dir (str): The directory path where images will be copied.
    csv_final_path (str): The file path where the final CSV will be saved.

    The function performs the following steps:
    1. Loads the CSV file into a DataFrame.
    2. Filters rows where 'terms' is 'shoes' and selects specific columns.
    3. Filters rows where 'section' is 'WOMAN' and removes incorrectly cataloged rows.
    4. Converts JSON strings in 'image_downloads' column to lists and calculates total images.
    5. Preprocesses images based on specific criteria and indices.
    6. Selects one image per row and finalizes column selection.
    7. Creates directories for images and text files, copies images, and generates text files.
    8. Saves the final DataFrame to a CSV file.
    """
    # Load the CSV file
    df = load_csv(csv_path)

    # Filter and select columns
    df_row_filtered = filter_rows(df, "terms =='shoes'")

    # Select relevant columns
    df_cols_selected = select_columns(df_row_filtered, ['name','description','price','currency','section','terms','image_downloads'])

    # Filter rows with section == WOMAN
    df_woman = filter_rows(df_cols_selected, "section =='WOMAN'").reset_index(drop=True)

     # Remove incorrect cataloged rows in df_woman
    df_woman_removed_rows = remove_incorrect_cataloged_rows(df_woman, [[273,274,275,276,277]])

    # Convert json to list in image_downloads
    df_woman_removed_rows.loc[:,'image_downloads']= df_woman_removed_rows['image_downloads'].apply(get_images_json_to_list)

    # get the total number of images
    df_woman_removed_rows.loc[:,'total_images'] = df_woman_removed_rows['image_downloads'].apply(len)

    # Preprocessing images
    #--------------------------------------------------------------------------------
    ## Image List Size: 27

    # fila: 261
    size=27
    indice_images = get_indices_images(df_woman_removed_rows,size)
    especial_indexes = [261]
    x= 6
    y=11
    w=0
    z=0

    preprocessing_woman_images(df_woman_removed_rows, indice_images, especial_indexes, x,y,w,z)

    ## Image List Size: 12
    # fila: 280
    size=12
    indice_images = get_indices_images(df_woman_removed_rows,size)
    especial_indexes = [280]
    x= 7
    y=11
    w=0
    z=0

    preprocessing_woman_images(df_woman_removed_rows, indice_images, especial_indexes, x,y,w,z)

    ## Image List Size: 11
    # filas: [98, 133, 192, 255, 263]
    size=11
    indice_images = get_indices_images(df_woman_removed_rows,size)
    especial_indexes = [192]
    x= 4
    y=8
    w=6
    z=10
    preprocessing_woman_images(df_woman_removed_rows, indice_images, especial_indexes, x,y,w,z)

    ## Image List Size: 10
    # filas: [64, 126, 144, 148, 176, 222, 235, 239, 243, 270, 272]
    size=10
    indice_images = get_indices_images(df_woman_removed_rows,size)
    especial_indexes = [148,235,239,270,272]
    x= 4
    y=9
    w=5
    z=9
    preprocessing_woman_images(df_woman_removed_rows, indice_images, especial_indexes, x,y,w,z)

    ## Image List Size: 9
    # filas: [0, 29, 60, 62, 65, 84, 85, 87, 95, 99, 105, 107, 113, 121, 123, 136, 137, 140, 166, 173, 184, 189, 190, 197, 201, 202, 205, 217, 218, 219, 221, 231, 236, 240, 244, 253, 254, 262, 274, 275, 276, 279]
    size=9
    indice_images = get_indices_images(df_woman_removed_rows,size)
    especial_indexes = [0,62,65,85,87,123,140,166,184,217,221]
    x= 3
    y=8
    w=4
    z=8
    preprocessing_woman_images(df_woman_removed_rows, indice_images, especial_indexes, x,y,w,z)

    ## Image List Size: 8
    # filas: 164
    indice_images = [164]
    especial_indexes = [164]
    x= 4
    y=8
    w=0
    z=0
    preprocessing_woman_images(df_woman_removed_rows, indice_images, especial_indexes, x,y,w,z)

    # filas: 31
    indice_images = [31]
    especial_indexes = [31]
    x= 1
    y=6
    w=0
    z=0
    preprocessing_woman_images(df_woman_removed_rows, indice_images, especial_indexes, x,y,w,z)

    # filas: [2, 21, 26, 31, 33, 40, 50, 51, 75, 79, 88, 92, 103, 109, 125, 131, 134, 138, 153, 156, 160, 164, 168, 169, 181, 186, 193, 194, 198, 203, 209, 210, 214, 215, 216, 228, 232, 238, 245, 249, 250, 251, 252, 258, 264]
    size=8
    indice_images = get_indices_images(df_woman_removed_rows,size)
    indice_images.remove(31)
    indice_images.remove(164)

    especial_indexes = [21,33,88,92,168,186,194,209,245,249]
    x=2
    y=7
    w=3
    z=8
    preprocessing_woman_images(df_woman_removed_rows, indice_images, especial_indexes, x,y,w,z)

    ## Image List Size: 7
    # filas: 112
    indice_images = [112]
    especial_indexes = [112]
    x= 0
    y=5
    w=0
    z=0
    preprocessing_woman_images(df_woman_removed_rows, indice_images, especial_indexes, x,y,w,z)

    # filas: [7, 11, 13, 14, 16, 18, 23, 24, 25, 27, 28, 30, 32, 34, 37, 38, 41, 42, 43, 47, 63, 66, 67, 68, 69, 70, 72, 74, 76, 81, 89, 94, 102, 110, 111, 112, 115, 119, 127, 129, 132, 135, 147, 150, 152, 155, 157, 161, 163, 171, 172, 174, 179, 185, 187, 188, 195, 196, 200, 206, 207, 223, 224, 229, 230, 233, 246, 247, 257, 268, 271, 273]
    size=7
    indice_images = get_indices_images(df_woman_removed_rows,size)
    indice_images.remove(112)
    especial_indexes = [13,18,63]
    x=3
    y=7
    w=2
    z=7
    preprocessing_woman_images(df_woman_removed_rows, indice_images, especial_indexes, x,y,w,z)

    ## Image List Size: 6
    indice_images_6 = [73,120,122,128,139,175,237]
    especial_indexes = [73,120,122,128,139,175,237]
    x= 2
    y=6
    w=0
    z=0
    preprocessing_woman_images(df_woman_removed_rows, indice_images_6, especial_indexes, x,y,w,z)

    # filas: [4, 8, 10, 22, 45, 48, 53, 54, 56, 58, 61, 71, 73, 78, 82, 83, 90, 96, 97, 100, 101, 108, 116, 117, 118, 120, 122, 128, 139, 141, 142, 145, 149, 151, 154, 170, 175, 177, 178, 180, 182, 191, 199, 204, 208, 211, 225, 226, 237, 248, 256, 259, 266, 267, 277]
    size=6
    indice_images = get_indices_images(df_woman_removed_rows,size)
    for i in indice_images_6:
        indice_images.remove(i)

    especial_indexes = [48,154,180,191,199,204]
    x=0
    y=5
    w=1
    z=6
    preprocessing_woman_images(df_woman_removed_rows, indice_images, especial_indexes, x,y,w,z)

    ## Image List Size: 5
    # filas: [1, 3, 5, 6, 9, 15, 17, 19, 20, 35, 39, 46, 49, 52, 55, 57, 59, 77, 80, 86, 91, 93, 104, 106, 114, 124, 130, 143, 158, 159, 162, 165, 167, 183, 212, 213, 220, 227, 234, 241, 242, 260, 265, 269, 278, 281]
    size=5
    indice_images = get_indices_images(df_woman_removed_rows,size)
    especial_indexes = [5,15,17,20,49,93,283]
    x=1
    y=5
    w=0
    z=5
    preprocessing_woman_images(df_woman_removed_rows, indice_images, especial_indexes, x,y,w,z)

    ## Image List Size: 4
    # filas: [12, 36, 146]
    size=4
    indice_images = get_indices_images(df_woman_removed_rows,size)
    especial_indexes = [12]
    x=1
    y=4
    w=0
    z=3
    preprocessing_woman_images(df_woman_removed_rows, indice_images, especial_indexes, x,y,w,z)

    ## Image List Size: 2
    #fila: 2 
    size=2
    indice_images = get_indices_images(df_woman_removed_rows,size)
    especial_indexes = [44]
    x=0
    y=1
    w=0
    z=0
    preprocessing_woman_images(df_woman_removed_rows, indice_images, especial_indexes, x,y,w,z)

    #--------------------------------------------------------------------------------

    # Get one image of list 
    df_woman_one_image = get_one_image_of_list_women(df_woman_removed_rows,0,2,3,1)

    # Select final columns
    df_woman_final_cols= select_columns(df_woman_one_image, ['name','description','price','currency','iso_image'])

    if not os.path.exists(txt_image_dir):
        # Create folder women_images
        create_folder(txt_image_dir)


    # Copy images of store_zara_data/images to folder women_images
    copy_images_to_folder(df_woman_final_cols, 'iso_image', origin_images_path, txt_image_dir)

    # Create txt files
    create_txt_files(df_woman_final_cols, txt_image_dir)

    # Save dataframe final 
    df_woman_final_cols.to_csv(csv_final_path, index=False)