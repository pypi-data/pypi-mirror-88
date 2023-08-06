from holon.protocols.http import Header

REFERENCE = "https://www.iana.org/go/rfc7232"


etag = Header(name="Etag", reference=REFERENCE)
last_modified = Header(name="Last-Modified", reference=REFERENCE)
if_match = Header(name="If-Match", reference=REFERENCE)
if_modified_since = Header(name="If-Modified-Since", reference=REFERENCE)
if_unmodified_since = Header(name="If-Unmodified-Since", reference=REFERENCE)
if_none_match = Header(name="If-None-Match", reference=REFERENCE)
