from jsonschema import Draft202012Validator

PATCH_SCHEMAS = {
    "CITATION": [
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Citation Link Patch",
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["op", "path", "value"],
                "properties": {
                    "op": {"const": "add"},
                    "path": {"const": "/links/-"},
                    "value": {
                        "type": "object",
                        "required": ["href", "type", "rel"],
                        "properties": {
                            "href": {"type": "string", "format": "uri"},
                            "type": {"const": "application/json"},
                            "rel": {"const": "cite-as"},
                        },
                        "additionalProperties": False,
                    },
                },
                "additionalProperties": False,
            },
        }
    ],
    "ERRATA": [
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Errata Link Patch",
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["op", "path", "value"],
                "properties": {
                    "op": {"const": "add"},
                    "path": {"const": "/links/-"},
                    "value": {
                        "type": "object",
                        "required": ["rel", "href", "title", "type"],
                        "properties": {
                            "rel": {"const": "related"},
                            "href": {"type": "string", "format": "uri"},
                            "title": {"const": "Errata issue"},
                            "type": {"enum": ["text/html", "application/json"]},
                        },
                        "additionalProperties": False,
                    },
                },
                "additionalProperties": False,
            },
        }
    ],
    "REPLICATE": [
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Replicate Asset Patch",
            "type": "array",
            "items": {
                "type": "object",
                "required": ["op", "path", "value"],
                "properties": {
                    "op": {"type": "string", "const": "add"},
                    "path": {
                        "type": "string",
                        "pattern": "^/assets/[^/]+/alternate/[^/]+$",
                    },
                    "value": {"type": "object"},
                },
                "additionalProperties": False,
            },
        }
    ],
    "CREATE": [
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Retract Patch",
            "type": "array",
            "minItems": 3,
            "maxItems": 3,
            "items": {
                "oneOf": [
                    {"$ref": "#/$defs/latest"},
                    {"$ref": "#/$defs/retracted"},
                    {"$ref": "#/$defs/assets"},
                ]
            },
            "allOf": [
                {"contains": {"$ref": "#/$defs/latest"}},
                {"contains": {"$ref": "#/$defs/retracted"}},
                {"contains": {"$ref": "#/$defs/assets"}},
            ],
            "$defs": {
                "latest": {
                    "type": "object",
                    "properties": {
                        "op": {"const": "replace"},
                        "path": {"const": "/properties/latest"},
                        "value": {"const": False},
                    },
                    "required": ["op", "path", "value"],
                    "additionalProperties": False,
                },
                "retracted": {
                    "type": "object",
                    "properties": {
                        "op": {"const": "replace"},
                        "path": {"const": "/properties/retracted"},
                        "value": {"const": True},
                    },
                    "required": ["op", "path", "value"],
                    "additionalProperties": False,
                },
                "assets": {
                    "type": "object",
                    "properties": {
                        "op": {"const": "replace"},
                        "path": {"const": "/assets"},
                        "value": {"type": "object", "maxProperties": 0},
                    },
                    "required": ["op", "path", "value"],
                    "additionalProperties": False,
                },
            },
        },
        {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": "Append Assets Patch",
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["op", "path", "value"],
                "properties": {
                    "op": {"const": "add"},
                    "path": {
                        "type": "string",
                        "pattern": "^/assets/[^/]+$",
                    },
                    "value": {
                        "allOf": [
                            {"$ref": "#/definitions/require_asset_fields"},
                            {"$ref": "#/definitions/asset_fields"},
                        ]
                    },
                },
                "additionalProperties": False,
            },
            "definitions": {
                "require_asset_fields": {
                    "$comment": "Please list all fields here so that we can force the existence of one of them in other parts of the schemas.",
                    "allOf": [
                        {"required": ["created"]},
                        {"required": ["protocol"]},
                        {
                            "if": {
                                "properties": {"type": {"const": "application/netcdf"}},
                                "required": ["type"],
                            },
                            "then": {
                                "required": [
                                    "file:size",
                                    "file:checksum",
                                    "file:local_path",
                                ]
                            },
                        },
                    ],
                },
                "asset_fields": {
                    "$comment": " Don't require fields here, do that above in the corresponding schema.",
                    "type": "object",
                    "properties": {
                        "protocol": {
                            "type": "string",
                            "enum": [
                                "http",
                                "https",
                                "globus",
                                "gridftp",
                                "kerchunk",
                                "netcdfsubset",
                                "opendap",
                                "wms",
                                "wps",
                                "s3",
                            ],
                        },
                        "cmip6:tracking_id": {
                            "type": "string",
                            "pattern": "^hdl:21\\.14100/[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$",
                        },
                    },
                },
            },
        },
    ],
}

PATCH_VALIDATORS: dict[str, Draft202012Validator] = {
    schema_name.upper(): [Draft202012Validator(schema) for schema in schemas]
    for schema_name, schemas in PATCH_SCHEMAS.items()
}
