Subject: F074-21 real formal PASS v2.datasets.Branch.delete
Created: 2026-10-21T23:43:25
Updated: 2026-10-21T23:43:25
---
Actual independent executor /root/formal074_prepare/independent_execute. Recorded by /root/formal074_finish_closure. v2.datasets.Branch.delete
Actual run 2026-10-21T12:48:52.893101+00:00 to 2026-10-21T12:48:54.357938+00:00; exit 0. Cases SHA256 599ee752c7c375d5afca7b12620527f74734f9e053f4e4c0060f3b6ecdfb6632; harness SHA256 ff6a8c6d15d25225c1c3a74755f73c7494011967968b652430d36a5a9ed72d05. SDK 1.101.0 source/module/method and current asset hashes match approved oracle.
Fresh httpx.MockTransport, fake independent-qa-074 credential, literal requests/results/errors. Socket connect/connect_ex/create_connection and DNS denied; explicit denial probes passed. Logs .ept/tmp/rest074_formal_execute.log SHA256 d4f695b522147d12976aaf2f2b41641d9eec1be26ecf185ae949ec1623e0e04c; full result JSON SHA256 a5052af29a75e92f3b5dbc2e13b0476a12c399eac492efddfff871c4c2892613.
Actual local discovery: {"case_id":"F074-21","operation":"v2.datasets.Branch.delete","checks":{"catalog_service_link":true,"index_exact_operation_contract":true,"contract_operation_heading":true,"contract_resource_guide_link":true,"behavior_method_heading":true,"behavior_example_link":true,"contract_model_definitions_resolve":true,"all_contract_local_links_resolve":true,"bound_asset_hashes":true},"catalog":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\catalog.md","sha256":"a2640d2c28ce15c8186af7c4525615a7cca32186783ca4079be0ed2424f492a7"},"index":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\v2\\datasets\\index.md","sha256":"afac0b160a87e8f945658f01301c93cd8c096887c03029cf1685fdd96449808a"},"contract":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\contracts\\v2\\datasets\\Branch\\delete.md","sha256":"dc80bcc80c5c3c7f49e86fb3c32d8a2b20e35ac409e22200bd190751eccc993e","heading":"# v2.datasets.Branch.delete"},"behavior":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\v2\\datasets\\Branch.md","sha256":"684ab53af97dcd66ca87e8dbc0dcf61bd622ab5df70349bf3bf7a147c0f611a8","heading":"### delete"},"example":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\\examples\
est\\074\\v2\\datasets\\Branch\\delete.py","sha256":"cb13ff089cfcb12e74f33d662284e0fec9eb1345441c32a48aa0a2a67b084c74"},"model_links":[{"label":"foundry_sdk._core.api_client.ResponseMode","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\ResponseMode.md","exists":true,"sha256":"cbc428d84d3ac081d7cb101d8ee383fdbfd9ed09dd938608c91ac3c8e269f35f"},{"label":"foundry_sdk._core.api_client.SdkInternal","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\SdkInternal.md","exists":true,"sha256":"c2b86183f885c076f0c3c8b9a7f190b89a97e92ddeef26ddd57db3d1ed1fa4ca"},{"label":"foundry_sdk._core.utils.RID","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\RID.md","exists":true,"sha256":"4af4eece28f34252abed320880118190a42c5cba5e72c27cd8dc8b72ecc223e2"},{"label":"foundry_sdk._core.utils.Timeout","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\Timeout.md","exists":true,"sha256":"1cd0a400d159d244916c364afaf160a1074016e2207d6bdd89e57f4292b3525a"},{"label":"foundry_sdk.v2.core.models.BranchName","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\core\\models\\BranchName.md","exists":true,"sha256":"c2dd02f85c66cc09e2f06ab9f5e88d0adc06f9bd7fd513a9a69282726c80ccde"},{"label":"foundry_sdk.v2.core.models.DatasetRid","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\core\\models\\DatasetRid.md","exists":true,"sha256":"869c7154829102a127dd874f449016d65044f1b669c3ab1cbafdd2142000b26d"},{"label":"foundry_sdk.v2.datasets.errors.BranchNotFound","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\errors\\BranchNotFound.md","exists":true,"sha256":"e097a7649fefdd8eaa0a61b38e3d198d18fec1ae285c529d704411f85a2a894f"},{"label":"foundry_sdk.v2.datasets.errors.BranchNotFoundParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\errors\\BranchNotFoundParameters.md","exists":true,"sha256":"d759d247f8fe49562251e8edf2223d6dda50481d451ffb0eabc35a4cb45887ab"},{"label":"foundry_sdk.v2.datasets.errors.DatasetNotFound","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\errors\\DatasetNotFound.md","exists":true,"sha256":"0ae8f0137ee4793f51ac9655735f9cddede2d52129fd4265879b335a7f0ca609"},{"label":"foundry_sdk.v2.datasets.errors.DatasetNotFoundParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\errors\\DatasetNotFoundParameters.md","exists":true,"sha256":"7e8102f3652f3e102258c1eda36b181f80a2847cf95ae4893202dad5bc0e0b76"},{"label":"foundry_sdk.v2.datasets.errors.DeleteBranchPermissionDenied","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\errors\\DeleteBranchPermissionDenied.md","exists":true,"sha256":"5a3db5a072bf12ce263d7edb04cb85751e5dc1934336a997954826c55b71dfa5"},{"label":"foundry_sdk.v2.datasets.errors.DeleteBranchPermissionDeniedParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\errors\\DeleteBranchPermissionDeniedParameters.md","exists":true,"sha256":"fa7d8c718cfed0c5fa13b81d060ea58f1674959692f1bb6e9d3964b24c381650"},{"label":"foundry_sdk.v2.datasets.errors.InvalidBranchName","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\errors\\InvalidBranchName.md","exists":true,"sha256":"7845d4417b4ad42f120e668cb27decf05e50bef0d8251ba6ec4dacf0db6e167f"},{"label":"foundry_sdk.v2.datasets.errors.InvalidBranchNameParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\errors\\InvalidBranchNameParameters.md","exists":true,"sha256":"fc309be52353cd6e563f61b331d6f5e5500ee260b173f533220aec40d1ae2f30"}]}
Actual assertion rows: [{"case_id":"F074-21","check":"success_typed","result":"PASS","requests":1},{"case_id":"F074-21","check":"success_raw_closed","result":"PASS","requests":1},{"case_id":"F074-21","check":"async_typed","result":"PASS","requests":1},{"case_id":"F074-21","check":"async_raw_closed","result":"PASS","requests":1},{"case_id":"F074-21","check":"error_BranchNotFound","result":"PASS","status":404,"requests":1},{"case_id":"F074-21","check":"error_DatasetNotFound","result":"PASS","status":404,"requests":1},{"case_id":"F074-21","check":"error_DeleteBranchPermissionDenied","result":"PASS","status":403,"requests":1},{"case_id":"F074-21","check":"error_InvalidBranchName","result":"PASS","status":400,"requests":1},{"case_id":"F074-21","check":"error_IndependentPermissionDenied","result":"PASS","status":401,"requests":1},{"case_id":"F074-21","check":"error_IndependentPermissionDenied","result":"PASS","status":403,"requests":1},{"case_id":"F074-21","check":"timeout_no_retry","result":"PASS","requests":1},{"case_id":"F074-21","check":"missing_required_dataset_rid","result":"PASS","requests":0},{"case_id":"F074-21","check":"missing_required_branch_name","result":"PASS","requests":0},{"case_id":"F074-21","check":"optional omission_typed","result":"PASS","requests":1},{"case_id":"F074-21","check":"optional omission_raw_closed","result":"PASS","requests":1},{"case_id":"F074-21","check":"required argument omitted","result":"PASS","requests":0}]
Offline serializer, typed/raw/stream/error and bounded control-flow evidence. Tenant effects and integrated J12 remain outside this execution.
