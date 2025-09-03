import pandas as pd
from pathlib import Path


def load_data(file_path=None, sheet_name=0, **kwargs):
    """
    Load the BDFO film analysis file (Excel or CSV) into a pandas dataframe.
    
    Parameters:
    -----------
    file_path : str, optional
        Path to the BDFO film analysis file. If None, uses the default path
        'examples/data/BDFO film analysis_2025-04-23.xlsx'
    sheet_name : str or int, default 0
        Name or index of the sheet to read (only for Excel files). Default is 0 (first sheet)
    **kwargs : additional arguments
        Additional arguments to pass to pd.read_excel() or pd.read_csv()
        
    Returns:
    --------
    pandas.DataFrame
        The loaded BDFO film analysis data
        
    Raises:
    -------
    FileNotFoundError
        If the file is not found at the specified path
    ValueError
        If the file format is not supported
    """
    
    # Set default file path if none provided
    if file_path is None:
        print("No file path provided")
    
    # Convert to Path object for better handling
    file_path = Path(file_path)
    
    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"BDFO film analysis file not found at: {file_path}")
    
    # Check file extension and load accordingly
    file_extension = file_path.suffix.lower()
    
    try:
        if file_extension in ['.xlsx', '.xls']:
            # Load Excel file
            df = pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)
            print(f"Successfully loaded BDFO film analysis Excel data from: {file_path}")
        elif file_extension == '.csv':
            # Load CSV file (ignore sheet_name parameter for CSV files)
            if 'sheet_name' in kwargs:
                kwargs.pop('sheet_name')  # Remove sheet_name from kwargs for CSV
            df = pd.read_csv(file_path, **kwargs)
            print(f"Successfully loaded BDFO film analysis CSV data from: {file_path}")
        else:
            raise ValueError(f"Unsupported file format: {file_extension}. Only .xlsx, .xls, and .csv files are supported.")
        
        print(f"Data shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        return df
        
    except Exception as e:
        print(f"Error loading BDFO film analysis data: {str(e)}")
        raise


def get_sheet_names(file_path=None):
    """
    Get the names of all sheets in the BDFO film analysis Excel file.
    
    Parameters:
    -----------
    file_path : str, optional
        Path to the BDFO film analysis Excel file. If None, uses the default path
        
    Returns:
    --------
    list
        List of sheet names in the Excel file (empty list for CSV files)
    """
    
    # Set default file path if none provided
    if file_path is None:
        current_dir = Path.cwd()
        file_path = current_dir / "examples" / "data" / "BDFO film analysis_2025-04-23.xlsx"
    
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"BDFO film analysis file not found at: {file_path}")
    
    # Check file extension
    file_extension = file_path.suffix.lower()
    
    try:
        if file_extension in ['.xlsx', '.xls']:
            # Get sheet names for Excel files
            excel_file = pd.ExcelFile(file_path)
            sheet_names = excel_file.sheet_names
            print(f"Available sheets in {file_path.name}: {sheet_names}")
            return sheet_names
        elif file_extension == '.csv':
            # CSV files don't have sheets
            print(f"CSV file {file_path.name} has no sheets (single table format)")
            return []
        else:
            raise ValueError(f"Unsupported file format: {file_extension}. Only .xlsx, .xls, and .csv files are supported.")
        
    except Exception as e:
        print(f"Error reading sheet names: {str(e)}")
        raise


def load_bdfo_data_with_info(file_path=None, sheet_name=0, **kwargs):
    """
    Load BDFO film analysis data and provide additional information about the dataset.
    
    Parameters:
    -----------
    file_path : str, optional
        Path to the BDFO film analysis file
    sheet_name : str or int, default 0
        Name or index of the sheet to read (only for Excel files)
    **kwargs : additional arguments
        Additional arguments to pass to pd.read_excel() or pd.read_csv()
        
    Returns:
    --------
    tuple
        (dataframe, info_dict) where info_dict contains basic statistics about the data
    """
    
    # Load the data
    df = load_data(file_path, sheet_name, **kwargs)
    
    # Create info dictionary
    info = {
        'shape': df.shape,
        'columns': list(df.columns),
        'dtypes': df.dtypes.to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'numeric_columns': df.select_dtypes(include=['number']).columns.tolist(),
        'categorical_columns': df.select_dtypes(include=['object']).columns.tolist(),
        'memory_usage': df.memory_usage(deep=True).sum()
    }
    
    # Add basic statistics for numeric columns
    if len(info['numeric_columns']) > 0:
        info['numeric_stats'] = df[info['numeric_columns']].describe().to_dict()
    
    print("\nDataset Information:")
    print(f"Shape: {info['shape']}")
    print(f"Memory usage: {info['memory_usage'] / 1024:.2f} KB")
    print(f"Numeric columns: {info['numeric_columns']}")
    print(f"Categorical columns: {info['categorical_columns']}")
    
    return df, info

