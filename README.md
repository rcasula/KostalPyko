# KostalPyko
This package is for working with a Piko (NOT Plenticore) Inverter from [Kostal](http://www.kostal-solar-electric.com/)

## Where has it been tested?
KostalPyko has been tested with a Kostal Piko 5.5. It should work with other Kostal inverters as well since they provide the same interface.

## Requirements
 * Requests
 * Python
 * lxml
 * httplib2
 * httpretty (for testing)
 
## Installing
```bash
$ pip install kostalpyko
```

## Usage
    from kostalpyko.kostalpyko import Piko
    
    #create a new piko instance
    p = Piko('host', 'username', 'password')
    
    #get current power 
    print(p.get_current_power())
    
    #get voltage from string 1
    print(p.get_string1_voltage())

## Thanks to
https://github.com/Tafkas since this packet is based on https://github.com/Tafkas/KostalPikoPy
