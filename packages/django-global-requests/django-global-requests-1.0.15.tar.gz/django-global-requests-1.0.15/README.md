# Django Global Requests

Allows for global request objects in your django project

## Installation

`pip install django-global-requests`

## Configuration

1. Add middleware:
    ```
    MIDDLEWARE = [
        ...
        'global_requests.GlobalRequestMiddleware',
    ]
    
    ```

## Usage

```
from global_requests import get_request
request = get_request()
```



  