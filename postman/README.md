# ArcGIS Postman Collection
## Overview

This collection provides calls to the Geometry service to get -

- the areas and lengths of a given array of polygons\*

- the remaining area/s left over from an intersection of a given polygon over an existing array of polygons


GET endpoints are given in this collection for these, although POSTs are available.

Note the query parameters are url encoded [https://www.url-encode-decode.com/](https://www.url-encode-decode.com/) can help with this. The advantage of using a GET is that the request can be posted into a URL where ArcGIS visualises the inputs into a form.

<img src="https://content.pstmn.io/7e8966f1-7b9f-4fb5-8604-5e053825b0c0/Z2VvbWV0cnkgc2VydmVyLnBuZw==">

## Public vs organisation specific URLs

The URLs used by these requests are from the ArcGIS **public** API e.g.

[https://utility.arcgisonline.com/arcgis/rest/services/Geometry/GeometryServer/intersect](https://utility.arcgisonline.com/arcgis/rest/services/Geometry/GeometryServer/intersect)

These do not require authentication and are intended for open non/limited commercial use.

A 'self' endpoint is included in the collection which is organisation specific and requires a token. Organisation specific endpoints require authentication e.g

[https://my-org.maps.arcgis.com/arcgis/rest/services/Geometry/GeometryServer/intersect](https://my-org.maps.arcgis.com/arcgis/rest/services/Geometry/GeometryServer/intersect)

These are more performant and are designed for commercial use. They can also access private data within the organisation account.

## Developer documentation
[self endpoint](https://developers.arcgis.com/rest/enterprise-administration/server/generatetoken/)<br>
[areas and lengths](https://developers.arcgis.com/rest/services-reference/enterprise/areas-and-lengths/)<br>
[intersections](https://developers.arcgis.com/rest/services-reference/enterprise/intersect.htm)<br>
[overview](https://developers.arcgis.com/documentation/)<br>
