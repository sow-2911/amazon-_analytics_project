# inspect_sqlite_tables.py
import sqlite3
import pandas as pd

def inspect_sqlite_database(db_path='amazon_india_analytics.db'):
    """
    Inspect all tables in SQLite database and return column names and data types
    
    Args:
        db_path (str): Path to SQLite database file
    """
    
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 Inspecting SQLite Database...")
        print("=" * 60)
        
        # Get list of all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        if not tables:
            print("❌ No tables found in the database!")
            return
        
        print(f"📊 Found {len(tables)} tables in the database:")
        print("-" * 60)
        
        # Inspect each table
        for table_info in tables:
            table_name = table_info[0]
            print(f"\n📋 Table: {table_name}")
            print("-" * 40)
            
            # Get column information
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            if not columns:
                print("   No columns found!")
                continue
            
            # Print column details
            print(f"{'Column Name':<25} {'Data Type':<15} {'Nullable':<10} {'Primary Key':<12}")
            print("-" * 65)
            
            for col in columns:
                col_id, col_name, col_type, not_null, default_val, pk = col
                nullable = "NO" if not_null else "YES"
                primary_key = "YES" if pk else "NO"
                print(f"{col_name:<25} {col_type:<15} {nullable:<10} {primary_key:<12}")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            row_count = cursor.fetchone()[0]
            print(f"\n   📈 Total Rows: {row_count:,}")
            
            # Show sample data (first 3 rows)
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
            sample_data = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            
            print(f"   🔍 Sample Data (first 3 rows):")
            if sample_data:
                # Print column headers
                header = " | ".join([f"{name:<15}" for name in column_names[:5]]) + ("..." if len(column_names) > 5 else "")
                print(f"   {header}")
                print("   " + "-" * len(header))
                
                # Print sample rows
                for row in sample_data:
                    row_display = " | ".join([f"{str(value)[:12]:<15}" for value in row[:5]]) + ("..." if len(row) > 5 else "")
                    print(f"   {row_display}")
            else:
                print("   No data available")
        
        print("\n" + "=" * 60)
        print("✅ Database inspection completed!")
        
        # Alternative method using pandas
        print("\n📊 Alternative Method - Using Pandas:")
        print("-" * 40)
        
        for table_info in tables:
            table_name = table_info[0]
            print(f"\n📋 Table: {table_name}")
            
            # Use pandas to get schema info
            try:
                df_sample = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 1", conn)
                print(f"   Columns: {len(df_sample.columns)}")
                print(f"   Data Types:")
                for col, dtype in df_sample.dtypes.items():
                    print(f"     - {col:<25}: {dtype}")
            except Exception as e:
                print(f"   Error reading table: {e}")
        
    except sqlite3.Error as e:
        print(f"❌ SQLite error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        # Close connection
        if conn:
            conn.close()
            print("\n🔒 Database connection closed.")

def get_detailed_schema(db_path='amazon_india_analytics.db'):
    """
    Get detailed schema information for all tables
    """
    try:
        conn = sqlite3.connect(db_path)
        
        # Get all tables
        tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = pd.read_sql_query(tables_query, conn)
        
        schema_info = {}
        
        for table_name in tables['name']:
            # Get column details
            pragma_query = f"PRAGMA table_info({table_name});"
            columns_df = pd.read_sql_query(pragma_query, conn)
            
            # Get sample data for data type validation
            sample_query = f"SELECT * FROM {table_name} LIMIT 5;"
            sample_df = pd.read_sql_query(sample_query, conn)
            
            schema_info[table_name] = {
                'columns': columns_df,
                'sample_data': sample_df,
                'row_count': len(pd.read_sql_query(f"SELECT * FROM {table_name}", conn))
            }
        
        return schema_info
        
    except Exception as e:
        print(f"Error getting detailed schema: {e}")
        return None
    finally:
        if conn:
            conn.close()

def export_schema_to_csv(db_path='amazon_india_analytics.db', output_file='database_schema.csv'):
    """
    Export database schema to CSV file
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        schema_data = []
        
        for table_info in tables:
            table_name = table_info[0]
            
            # Get column information
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            
            for col in columns:
                col_id, col_name, col_type, not_null, default_val, pk = col
                schema_data.append({
                    'table_name': table_name,
                    'column_name': col_name,
                    'data_type': col_type,
                    'nullable': 'NO' if not_null else 'YES',
                    'primary_key': 'YES' if pk else 'NO',
                    'default_value': default_val
                })
        
        # Create DataFrame and export to CSV
        schema_df = pd.DataFrame(schema_data)
        schema_df.to_csv(output_file, index=False)
        print(f"✅ Schema exported to: {output_file}")
        
        return schema_df
        
    except Exception as e:
        print(f"Error exporting schema: {e}")
        return None
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🚀 SQLite Database Inspector")
    print("=" * 50)
    
    # You can change the database path if needed
    db_path = 'amazon_india_analytics.db'  # Change this if your DB has different name
    
    # Method 1: Basic inspection
    inspect_sqlite_database(db_path)
    
    print("\n" + "=" * 60)
    print("📋 DETAILED SCHEMA ANALYSIS")
    print("=" * 60)
    
    # Method 2: Detailed schema analysis
    schema_info = get_detailed_schema(db_path)
    
    if schema_info:
        for table_name, info in schema_info.items():
            print(f"\n🎯 Table: {table_name}")
            print(f"   📊 Total Rows: {info['row_count']:,}")
            print(f"   📋 Columns ({len(info['columns'])}):")
            
            for _, col in info['columns'].iterrows():
                pk_indicator = " 🔑" if col['pk'] else ""
                nullable_indicator = "" if col['notnull'] else " ❓"
                print(f"     - {col['name']:<25} ({col['type']:<15}){pk_indicator}{nullable_indicator}")
    
    print("\n" + "=" * 60)
    print("💾 EXPORTING SCHEMA TO CSV")
    print("=" * 60)
    
    # Method 3: Export to CSV
    export_schema_to_csv(db_path)
    
    print("\n🎉 Database inspection completed successfully!")