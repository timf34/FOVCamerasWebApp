## Deploying to AWS EB 

1. Build ReactJS client
    - `cd client`
    - `npm run build`
1. Move build folder to server folder
    - `mv build/ server/`
    - Or just copy, paste, etc.
1. Create a zip file of the server folder
    - `zip -r server.zip server/`
    - Or just right click and compress
      - Ensure to not select the `Dockerfile`, `/venv`, `/aws_zips` or `.dockerignore` when compressing
