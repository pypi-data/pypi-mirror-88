# coding:utf-8
from __future__ import print_function

from ttvcloud.imagex.ImageXService import ImageXService

if __name__ == '__main__':
    imagex_service = ImageXService()

    # call below method if you dont set ak and sk in $HOME/.vcloud/config
    imagex_service.set_ak('AKLTNWYyY2EzZjY4NWU4NGYzNzg1YzFhMGI0NmQ2OWQzODU')
    imagex_service.set_sk('oXnm9XFabLxlxHqF1UtYvFLDSb9nevX5z0bBOHU9H32Wo0CrvzzhJzk315nfVh5v')

    # service id list allowed to do upload, set to empty if no restriction
    service_ids = ['19tz3ytenx']

    resp = imagex_service.get_upload_auth(service_ids)
    print(resp)
