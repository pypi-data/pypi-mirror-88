# soapsnow
Python client for interacting with the ServiceNow SOAP web service.

## API Documentation
For information about the ServiceNow SOAP web service, see the [description](https://docs.servicenow.com/bundle/london-application-development/page/integrate/inbound-soap/concept/c_SOAPWebService.html) and [API Functions](https://docs.servicenow.com/bundle/paris-application-development/page/integrate/web-services-apis/reference/r_DirectWebServiceAPIFunctions.html).

## Install
```bash
pip3 install soapsnow --user
```

## Usage
```python
from soapsnow import SOAPSnow

user = 'user'
pwd  = 'pwd'
inst = 'customer'
url  = f'https://{inst}.service-now.com/incident.do?SOAP&displayvalue=true'
snow = SOAPSnow(user, pwd, url)

resp = snow.do('getRecords', number='INC000123')
print(resp)

resp = snow.do(
    method='insert',
    number='INC000123',
    state='resolved',
    work_notes='Test'
)
print(resp)

resp = snow.do(
    method='getRecords',
    assignment_group='my-group',
    active=1,
    __encoded_query='state!=6^short_descriptionLIKEHost is unreachable',
    __limit=20
)
print(resp)
```

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.