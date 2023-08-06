# dns_zone_builder

This Python package makes creating DNS zone files from within Python code easier.

The basic idea is to create an instance of the DnsZoneBuilder class, add resource records to it (with the add_xx_rr methods) and then print the instance into a file to use with a BIND name server.

If you don't specify a serial number, one will be created for you. It will be today's date followed by a counter that is incremented every 15 minutes (so it will go from 00 to 95).

As an added bonus, when creating a normal "forward" zone, you can add one or more network specifications (IPv4 or IPv6) to have reverse zones created for you (with the same SOA and NS information).

Refer to the main code for an example on how to use it.