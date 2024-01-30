

import flightplandb as fpdb
import asyncio

# obviously, substitute your own token
API_KEY = "8Pj8klqL2zgJE8VDrkQQqZ46VhbA2oAA0FxkYSqK"


import flightplandb as fpdb
import asyncio
import polyline

# obviously, substitute your own token
API_KEY = "8Pj8klqL2zgJE8VDrkQQqZ46VhbA2oAA0FxkYSqK"

async def main():
    
    # for testing purposes

    plan = await fpdb.plan.decode("KBNA TAZMO3 BURME VXV IDDAA Q64 SAWED Q97 DLAAY RADDS SIE CAMRN4 KJFK",key=API_KEY)


  
    pl = plan.encodedPolyline
    print(polyline.decode(pl, 5))

asyncio.run(main())


#asyncio.run(print(fpdb.plan.decode("KBNA TAZMO3 BURME VXV IDDAA Q64 SAWED Q97 DLAAY RADDS SIE CAMRN4 KJFK",key=API_KEY)))