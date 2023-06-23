from django.http import JsonResponse, HttpResponse
from sqlalchemy import create_engine, MetaData, select, func, text

# Handler for the /connect/<path:db_url> endpoint
def connectView(request, db_url):
    # Try a connection with the given URL
    try:
        engine = create_engine(db_url)
    except Exception as err:
        return HttpResponse(f'Error: {err}')

    # Crafting the response
    dbMetadata = []
    dbName = engine.url.database

    # Get the schema names using a SQL query
    schemaNames = []
    with engine.connect() as conn:
        query = "SELECT schema_name FROM information_schema.schemata"
        result = conn.execute(text(query))

        # Iterate over the result and appends schema names to the list
        for row in result:
            schemaNames.append(row[0])

        # Close the resultset
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

                # Parse number of rows
                num_rows = table.info.get('rows')
                if num_rows is None:
                    # If the number of rows is not specified, query the table
                    try:
                        query = select(func.count()).select_from(text(table.name))
                        num_rows = conn.execute(query).scalar()
                    except Exception as err:
                        # Display -1 if the query fails 
                        num_rows = -1 

                # Craft the table metadata     
                tableMetadata = {
                    'columns': colMetadata, 
                    'num_rows': num_rows, 
                    'schema': schemaName,
                    'database': dbName
                }

                dbMetadata.append(tableMetadata)
    return JsonResponse({'metadata': dbMetadata})
