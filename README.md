# apt4989-api
API Wrapper for APT4989

#### docker-compose.yaml
```yaml
services:
  apt4989-api:
    image: apt4989-api
    container_name: apt4989-api
    ports:
      - 8000:8000
    environment:
      API_KEY: apiKEY
      MDB_PATH: /path/to/mounted/apt4989.mdb
      MDB_PASSWORD: passw0rd
    volumes:
      - /path/to/original/apt4989.mdb:/path/to/mounted/apt4989.mdb
```