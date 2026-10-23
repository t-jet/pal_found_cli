Subject: F074-03 real formal PASS v1.datasets.Branch.get
Created: 2026-10-21T23:43:20
Updated: 2026-10-21T23:43:20
---
Actual independent executor /root/formal074_prepare/independent_execute. Recorded by /root/formal074_finish_closure. v1.datasets.Branch.get
Actual run 2026-10-21T12:48:52.893101+00:00 to 2026-10-21T12:48:54.357938+00:00; exit 0. Cases SHA256 599ee752c7c375d5afca7b12620527f74734f9e053f4e4c0060f3b6ecdfb6632; harness SHA256 ff6a8c6d15d25225c1c3a74755f73c7494011967968b652430d36a5a9ed72d05. SDK 1.101.0 source/module/method and current asset hashes match approved oracle.
Fresh httpx.MockTransport, fake independent-qa-074 credential, literal requests/results/errors. Socket connect/connect_ex/create_connection and DNS denied; explicit denial probes passed. Logs .ept/tmp/rest074_formal_execute.log SHA256 d4f695b522147d12976aaf2f2b41641d9eec1be26ecf185ae949ec1623e0e04c; full result JSON SHA256 a5052af29a75e92f3b5dbc2e13b0476a12c399eac492efddfff871c4c2892613.
Actual local discovery: {"case_id":"F074-03","operation":"v1.datasets.Branch.get","checks":{"catalog_service_link":true,"index_exact_operation_contract":true,"contract_operation_heading":true,"contract_resource_guide_link":true,"behavior_method_heading":true,"behavior_example_link":true,"contract_model_definitions_resolve":true,"all_contract_local_links_resolve":true,"bound_asset_hashes":true},"catalog":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\catalog.md","sha256":"a2640d2c28ce15c8186af7c4525615a7cca32186783ca4079be0ed2424f492a7"},"index":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\v1\\datasets\\index.md","sha256":"559f526c22d5aeafdede99f095e8a98d34023f78b38e6d0c57aed4968af488f3"},"contract":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\contracts\\v1\\datasets\\Branch\\get.md","sha256":"a7787f87dda1693b4163b6c2c752ffe1b0af43a5a35ba20f3a555b32867a6d07","heading":"# v1.datasets.Branch.get"},"behavior":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\v1\\datasets\\Branch.md","sha256":"1e83108112ce99de3c7a0e6186ec8eef9f33d4e88745123fe3e670d3ca37f49c","heading":"### get"},"example":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\\examples\
est\\074\\v1\\datasets\\Branch\\get.py","sha256":"6b33da63243164031f18e0085e0d0faaa7913d89eea113e662dbcf12ce8f5235"},"model_links":[{"label":"foundry_sdk._core.api_client.ResponseMode","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\ResponseMode.md","exists":true,"sha256":"cbc428d84d3ac081d7cb101d8ee383fdbfd9ed09dd938608c91ac3c8e269f35f"},{"label":"foundry_sdk._core.api_client.SdkInternal","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\SdkInternal.md","exists":true,"sha256":"c2b86183f885c076f0c3c8b9a7f190b89a97e92ddeef26ddd57db3d1ed1fa4ca"},{"label":"foundry_sdk._core.model_base.ModelBase","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\ModelBase.md","exists":true,"sha256":"5f5b16aa4764220b3b6b9c4287c5bb45e46b9cbe122d8965f7a6461b0e030587"},{"label":"foundry_sdk._core.utils.RID","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\RID.md","exists":true,"sha256":"4af4eece28f34252abed320880118190a42c5cba5e72c27cd8dc8b72ecc223e2"},{"label":"foundry_sdk._core.utils.Timeout","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\Timeout.md","exists":true,"sha256":"1cd0a400d159d244916c364afaf160a1074016e2207d6bdd89e57f4292b3525a"},{"label":"foundry_sdk.v1.datasets.errors.BranchNotFound","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\BranchNotFound.md","exists":true,"sha256":"97855c730b4ff55ad277b6f32567a134c9d41013dba7f3572611941afa2d33ab"},{"label":"foundry_sdk.v1.datasets.errors.BranchNotFoundParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\BranchNotFoundParameters.md","exists":true,"sha256":"1a9cb75734453404a44e52d5132fc56582b3e4148a5bc07b4ae3e5767aac347c"},{"label":"foundry_sdk.v1.datasets.errors.DatasetNotFound","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\DatasetNotFound.md","exists":true,"sha256":"675645f37e488c5609ac1f1c9343745130f7be9b1823301eddf250021ee51c95"},{"label":"foundry_sdk.v1.datasets.errors.DatasetNotFoundParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\DatasetNotFoundParameters.md","exists":true,"sha256":"8a10c7f77e7d5db9e8efc93ca0177311132451cbb755db5f60b06d02ef9d1f26"},{"label":"foundry_sdk.v1.datasets.models.Branch","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\models\\Branch.md","exists":true,"sha256":"d3fd2a8013fd0bbcbf7b9da9fc9d69f664520115054b58dcb50388b172cf3596"},{"label":"foundry_sdk.v1.datasets.models.BranchId","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\models\\BranchId.md","exists":true,"sha256":"1e1d4b0aaa8f9e79865671f0df6791deda0dda20a0ca9fb973b01d9c420224d7"},{"label":"foundry_sdk.v1.datasets.models.DatasetRid","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\models\\DatasetRid.md","exists":true,"sha256":"31c5609cfff2d2d6a72113faf6fe0519648b43b3ac42f3f38e1f8ed630f680c2"},{"label":"foundry_sdk.v1.datasets.models.TransactionRid","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\models\\TransactionRid.md","exists":true,"sha256":"b77855a6ab9595d0ea97c6fd304e3f9eb54ad1ec86881957255e7993d715474c"}]}
Actual assertion rows: [{"case_id":"F074-03","check":"success_typed","result":"PASS","requests":1},{"case_id":"F074-03","check":"success_raw_closed","result":"PASS","requests":1},{"case_id":"F074-03","check":"async_typed","result":"PASS","requests":1},{"case_id":"F074-03","check":"async_raw_closed","result":"PASS","requests":1},{"case_id":"F074-03","check":"sync_stream_closed","result":"PASS","requests":1},{"case_id":"F074-03","check":"async_stream_closed","result":"PASS","requests":1},{"case_id":"F074-03","check":"error_BranchNotFound","result":"PASS","status":404,"requests":1},{"case_id":"F074-03","check":"error_DatasetNotFound","result":"PASS","status":404,"requests":1},{"case_id":"F074-03","check":"error_IndependentPermissionDenied","result":"PASS","status":401,"requests":1},{"case_id":"F074-03","check":"error_IndependentPermissionDenied","result":"PASS","status":403,"requests":1},{"case_id":"F074-03","check":"timeout_no_retry","result":"PASS","requests":1},{"case_id":"F074-03","check":"malformed_json","result":"PASS"},{"case_id":"F074-03","check":"missing_required_dataset_rid","result":"PASS","requests":0},{"case_id":"F074-03","check":"missing_required_branch_id","result":"PASS","requests":0},{"case_id":"F074-03","check":"optional omission_typed","result":"PASS","requests":1},{"case_id":"F074-03","check":"optional omission_raw_closed","result":"PASS","requests":1},{"case_id":"F074-03","check":"required argument omitted","result":"PASS","requests":0}]
Offline serializer, typed/raw/stream/error and bounded control-flow evidence. Tenant effects and integrated J12 remain outside this execution.
