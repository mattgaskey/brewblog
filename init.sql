DO
$$
BEGIN
   -- Log the start of the script
   RAISE NOTICE 'Starting init.sql script';

   -- Check if the role exists
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'postgres') THEN
      -- Log the creation of the role
      RAISE NOTICE 'Creating role postgres';
      CREATE ROLE postgres WITH LOGIN PASSWORD 'postgres';
      -- Log the alteration of the role
      RAISE NOTICE 'Altering role postgres to have CREATEDB';
      ALTER ROLE postgres CREATEDB;
   ELSE
      -- Log that the role already exists
      RAISE NOTICE 'Role postgres already exists';
   END IF;

   -- Log the end of the script
   RAISE NOTICE 'Finished init.sql script';
END
$$;