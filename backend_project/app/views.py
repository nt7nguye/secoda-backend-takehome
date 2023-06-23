from django.http import JsonResponse, HttpResponse
from sqlalchemy import create_engine, MetaData, select, func, text

# Handler for the /connect/<path:db_url> endpoint
def connectView(request, db_url):
    # Try a connection with the given URL
    try:
        engine = create_engine(db_url)
    except Exception as err:
        return HttpResponse(f'DB URL error: {err}')

    # Crafting the response
    dbMetadata = []
    dbName = engine.url.database

    with engine.connect() as conn:
        # Get the schema names using a SQL query
        schemaNames = []
        query = "SELECT schema_name FROM information_schema.schemata"
        result = conn.execute(text(query))

        # Iterate over the result and appends schema names to the list
        for row in result:
            schemaNames.append(row[0])

        # Close the resultset
        result.close()

        # Get approx stats of number of rows in each schema
        numRowsResult = {}
        query = "SELECT schemaname,relname,n_live_tup \
                FROM pg_stat_all_tables  \
                ORDER BY n_live_tup DESC;"
        result = conn.execute(text(query))

        # Fetch rows of the query and iterate through them
        rows = result.fetchall()
        for row in rows:
            schemaName = row[0]
            tableName = row[1]
            num_rows = row[2]

            # If the schema is not in the dictionary, add it
            if schemaName not in numRowsResult:
                numRowsResult[schemaName] = {}

            # Add the table name and number of rows to the dictionary
            numRowsResult[schemaName][tableName] = num_rows
        result.close()

        # Get a metadata object for the database 
        metadata = MetaData()

        # Get all tables in each schema 
        for schemaName in schemaNames:
            # Reflect the database schema
            metadata.reflect(engine, schema=schemaName)

            # Iterating through the metadata of each table in db
            for table in metadata.tables.values():
                # Parse columns
                colMetadata = []
                for col in table.columns.values():
                    colMetadata.append({
                        'name': col.name,
                        'type': str(col.type)
                    })
                
                # Get number of rows
                try:
                    numRows = numRowsResult[schemaName][table.name]
                except KeyError:
                    # numRows calculation is an approximation
                    numRows = -1

                # Craft the table metadata     
                tableMetadata = {
                    'name': table.name, # Not required but useful for debugging
                    'columns': colMetadata, 
                    'num_rows': numRows, 
                    'schema': schemaName,
                    'database': dbName
                }

                dbMetadata.append(tableMetadata)
    return JsonResponse({'metadata': dbMetadata})
