The idea behind this package is possibility to you use some client or something like the Metabase for collect and analyse logs of your application.  
  
Its need two environments variables:  
* MONGO_DB  
* MONGO_URL      

Its works with three collections:  
* error  
* info  
* critical

Sample:
~~~python
from mongo_system_log import *
log = LogThis(get_module_name())
log.info('error message', payload='payload', result='result')
log.error('error message', payload='payload', result='result')
log.critical('error message', payload='payload', result='result')
~~~
get_module_name()  
* This function gets module and file name that called it. Must be called on instantiate the LogThis class.  
The arguments **payload** and **result** has default value None.
