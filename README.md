#Jenkins Slave check script

This script makes simple calls to the JSON API that Jenkins masters expose in order
to check on the existing connected slaves. Anything considered offline, whether that's
due to a disconnect or manual intervention, will be reported.