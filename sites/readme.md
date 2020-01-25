## API


### Области поиска

#### Список

**Request**

    GET /api/v1/geobot/search_area/
    
**Response**

    HTTP/1.1 200 OK
    Content-Type: application/json
    
    [
        {
            "name": (str)
        },
        ...
    ]


### История

#### Список

**Request**

    GET /api/v1/geobot/history/
    
    params:
        user: (int)
        page: (int)
        page_size: (int)
        
**Response**

    HTTP/1.1 200 OK
    Content-Type: application/json
    
    {
        "count": (int),
        "next": (str),
        "previous": (str),
        "results": [
            {
                "date": (date),
                "request": (str),
                "result": (str),
                "user": (str)
            },
            ...
        ]
    }


#### Добавление

**Request**

    POST /api/v1/geobot/history/ HTTP/1.1
    Content-Type: application/json
    
    {
        "request": (str),
        "result": (str),
        "user": (str)
    }
        
**Response**

    HTTP/1.1 201 Created
    Content-Type: application/json
    
    {
        "date": (date),
        "request": (str),
        "result": (str),
        "user": (str)
    }
