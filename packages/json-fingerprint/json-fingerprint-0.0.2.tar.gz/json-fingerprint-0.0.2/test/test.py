import json
import json_fingerprint as jf

obj = [
    3,
    1,
    2,
    "a"
]

obj_str = json.dumps(obj)
jfpv1 = jf.json_fingerprint(obj_str, hash_function='sha256', version=1)
print(jfpv1)
