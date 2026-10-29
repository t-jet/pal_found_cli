Subject: F074-25 real formal PASS v2.datasets.Dataset.create
Created: 2026-10-21T23:43:26
Updated: 2026-10-21T23:43:26
---
Actual independent executor /root/formal074_prepare/independent_execute. Recorded by /root/formal074_finish_closure. v2.datasets.Dataset.create
Actual run 2026-10-21T12:48:52.893101+00:00 to 2026-10-21T12:48:54.357938+00:00; exit 0. Cases SHA256 599ee752c7c375d5afca7b12620527f74734f9e053f4e4c0060f3b6ecdfb6632; harness SHA256 ff6a8c6d15d25225c1c3a74755f73c7494011967968b652430d36a5a9ed72d05. SDK 1.101.0 source/module/method and current asset hashes match approved oracle.
Fresh httpx.MockTransport, fake independent-qa-074 credential, literal requests/results/errors. Socket connect/connect_ex/create_connection and DNS denied; explicit denial probes passed. Logs .ept/tmp/rest074_formal_execute.log SHA256 d4f695b522147d12976aaf2f2b41641d9eec1be26ecf185ae949ec1623e0e04c; full result JSON SHA256 a5052af29a75e92f3b5dbc2e13b0476a12c399eac492efddfff871c4c2892613.
Actual local discovery: {"case_id":"F074-25","operation":"v2.datasets.Dataset.create","checks":{"catalog_service_link":true,"index_exact_operation_contract":true,"contract_operation_heading":true,"contract_resource_guide_link":true,"behavior_method_heading":true,"behavior_example_link":true,"contract_model_definitions_resolve":true,"all_contract_local_links_resolve":true,"bound_asset_hashes":true},"catalog":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\catalog.md","sha256":"a2640d2c28ce15c8186af7c4525615a7cca32186783ca4079be0ed2424f492a7"},"index":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\v2\\datasets\\index.md","sha256":"afac0b160a87e8f945658f01301c93cd8c096887c03029cf1685fdd96449808a"},"contract":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\contracts\\v2\\datasets\\Dataset\\create.md","sha256":"de296eb08e21de2346f6e036f38c3970b2b179a7686b5b5f6a32b87b1637850a","heading":"# v2.datasets.Dataset.create"},"behavior":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\v2\\datasets\\Dataset.md","sha256":"c8896fac6c97cd01d174b2ef67ccfc49798ca02e64761f5ce487d2e28f8ff6ec","heading":"### create"},"example":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\\examples\
est\\074\\v2\\datasets\\Dataset\\create.py","sha256":"1293be13fba5e6a82197cbabb4d7d1ed3fa295969d48c8aaa87255507e9851b5"},"model_links":[{"label":"foundry_sdk._core.api_client.ResponseMode","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\ResponseMode.md","exists":true,"sha256":"cbc428d84d3ac081d7cb101d8ee383fdbfd9ed09dd938608c91ac3c8e269f35f"},{"label":"foundry_sdk._core.api_client.SdkInternal","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\SdkInternal.md","exists":true,"sha256":"c2b86183f885c076f0c3c8b9a7f190b89a97e92ddeef26ddd57db3d1ed1fa4ca"},{"label":"foundry_sdk._core.model_base.ModelBase","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\ModelBase.md","exists":true,"sha256":"5f5b16aa4764220b3b6b9c4287c5bb45e46b9cbe122d8965f7a6461b0e030587"},{"label":"foundry_sdk._core.utils.RID","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\RID.md","exists":true,"sha256":"4af4eece28f34252abed320880118190a42c5cba5e72c27cd8dc8b72ecc223e2"},{"label":"foundry_sdk._core.utils.Timeout","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\Timeout.md","exists":true,"sha256":"1cd0a400d159d244916c364afaf160a1074016e2207d6bdd89e57f4292b3525a"},{"label":"foundry_sdk.v2.core.models.BranchName","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\core\\models\\BranchName.md","exists":true,"sha256":"c2dd02f85c66cc09e2f06ab9f5e88d0adc06f9bd7fd513a9a69282726c80ccde"},{"label":"foundry_sdk.v2.core.models.DatasetRid","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\core\\models\\DatasetRid.md","exists":true,"sha256":"869c7154829102a127dd874f449016d65044f1b669c3ab1cbafdd2142000b26d"},{"label":"foundry_sdk.v2.datasets.errors.BranchAlreadyExists","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\errors\\BranchAlreadyExists.md","exists":true,"sha256":"bf0057b75bc0962b44a14d887ac856fa8f9ccae83258fc819bfd6b601180b8f1"},{"label":"foundry_sdk.v2.datasets.errors.BranchAlreadyExistsParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\errors\\BranchAlreadyExistsParameters.md","exists":true,"sha256":"cf41295d7a4dd73207b1bd8c8cb3a5cefc2395cbd71040e65a1678c4559d15bc"},{"label":"foundry_sdk.v2.datasets.errors.CreateBranchPermissionDenied","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\errors\\CreateBranchPermissionDenied.md","exists":true,"sha256":"04b26a268af489846e0827d45da31cfcb2461611f72f55a0e84b8ff99b32d7ec"},{"label":"foundry_sdk.v2.datasets.errors.CreateBranchPermissionDeniedParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\errors\\CreateBranchPermissionDeniedParameters.md","exists":true,"sha256":"8c2395a2fc32f9a03c09706539e639045cfec8736395f5f9efe1246e8cbdb56f"},{"label":"foundry_sdk.v2.datasets.errors.CreateDatasetPermissionDenied","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\errors\\CreateDatasetPermissionDenied.md","exists":true,"sha256":"446b82af53fd03f1c161a4f88928f6b26dc8d3c586923d6770c303bfa501b570"},{"label":"foundry_sdk.v2.datasets.errors.CreateDatasetPermissionDeniedParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\errors\\CreateDatasetPermissionDeniedParameters.md","exists":true,"sha256":"74a6f66d417c03f9426aa4c5fd67379514bd444cf82d6504b54afc8fa62c3772"},{"label":"foundry_sdk.v2.datasets.errors.DatasetNotFound","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\errors\\DatasetNotFound.md","exists":true,"sha256":"0ae8f0137ee4793f51ac9655735f9cddede2d52129fd4265879b335a7f0ca609"},{"label":"foundry_sdk.v2.datasets.errors.DatasetNotFoundParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\errors\\DatasetNotFoundParameters.md","exists":true,"sha256":"7e8102f3652f3e102258c1eda36b181f80a2847cf95ae4893202dad5bc0e0b76"},{"label":"foundry_sdk.v2.datasets.errors.InvalidBranchName","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\errors\\InvalidBranchName.md","exists":true,"sha256":"7845d4417b4ad42f120e668cb27decf05e50bef0d8251ba6ec4dacf0db6e167f"},{"label":"foundry_sdk.v2.datasets.errors.InvalidBranchNameParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\errors\\InvalidBranchNameParameters.md","exists":true,"sha256":"fc309be52353cd6e563f61b331d6f5e5500ee260b173f533220aec40d1ae2f30"},{"label":"foundry_sdk.v2.datasets.errors.TransactionNotCommitted","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\errors\\TransactionNotCommitted.md","exists":true,"sha256":"faa7a2ca9e8c9157244485a8ed20834c5f8b5d86a9b72fdaa26c4187217cd19b"},{"label":"foundry_sdk.v2.datasets.errors.TransactionNotCommittedParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\errors\\TransactionNotCommittedParameters.md","exists":true,"sha256":"51a058ed423b0aec4e543da773cb2766d3a2ff1e5c858116b5f80d810f9db86a"},{"label":"foundry_sdk.v2.datasets.errors.TransactionNotFound","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\errors\\TransactionNotFound.md","exists":true,"sha256":"573d70ede0b97cf1a0a98e41654aae6070d0d28387527a40e9aae103a23a3559"},{"label":"foundry_sdk.v2.datasets.errors.TransactionNotFoundParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\errors\\TransactionNotFoundParameters.md","exists":true,"sha256":"70de33a6d930381be1ca001773ee1a03c13ca7430820e5ea299203d9b4d61545"},{"label":"foundry_sdk.v2.datasets.models.CreateDatasetRequest","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\models\\CreateDatasetRequest.md","exists":true,"sha256":"f77421cc3054633928f11400826bbe5daafafd2774048c959cb1f4778808f784"},{"label":"foundry_sdk.v2.datasets.models.Dataset","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\models\\Dataset.md","exists":true,"sha256":"77c6d0146ec7c252a650314c0ea419717048eb488a8d37d390a9ca4e36fa34bd"},{"label":"foundry_sdk.v2.datasets.models.DatasetName","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\models\\DatasetName.md","exists":true,"sha256":"f8f104f0c77e75f37843343cf955b638e7be0259f2ad47e416e84fc3b0c0aa19"},{"label":"foundry_sdk.v2.datasets.models.TransactionRid","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\models\\TransactionRid.md","exists":true,"sha256":"07d4e6050900c414482f9fd89eb8a05594a9aeafc4cca026cec040c91ec3c78a"},{"label":"foundry_sdk.v2.datasets.models.TransactionStatus","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\datasets\\models\\TransactionStatus.md","exists":true,"sha256":"b66f4556cf0130aa141c4bb1efe0f4c87942e9f4f1bf8399bce1f281bf1b2b3e"},{"label":"foundry_sdk.v2.filesystem.errors.FolderNotFound","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\filesystem\\errors\\FolderNotFound.md","exists":true,"sha256":"c837e92f1190c48a16edc1f1091ed34b2d21fd99fd872c7e3d70ae1f204abeab"},{"label":"foundry_sdk.v2.filesystem.errors.FolderNotFoundParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\filesystem\\errors\\FolderNotFoundParameters.md","exists":true,"sha256":"948e1d8d722ee4d80be9a03eb4262a74443de9e78989671ca1e2547e30fcbdaf"},{"label":"foundry_sdk.v2.filesystem.errors.InvalidDisplayName","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\filesystem\\errors\\InvalidDisplayName.md","exists":true,"sha256":"5cc3f4f170a80cc1076b3f8ab6eb2c93a3c1f78d0f9edfe42df0fac94e2e1329"},{"label":"foundry_sdk.v2.filesystem.errors.InvalidDisplayNameParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\filesystem\\errors\\InvalidDisplayNameParameters.md","exists":true,"sha256":"6f66d11dd2f9a8ea784449899f11896ae087db6f2174a21700e64d2dc31a9caf"},{"label":"foundry_sdk.v2.filesystem.errors.ResourceNameAlreadyExists","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\filesystem\\errors\\ResourceNameAlreadyExists.md","exists":true,"sha256":"e0775cea800ee17f00e0a7343759a7f90d5036b1118b5937064429a8a3e98b3d"},{"label":"foundry_sdk.v2.filesystem.errors.ResourceNameAlreadyExistsParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\filesystem\\errors\\ResourceNameAlreadyExistsParameters.md","exists":true,"sha256":"444d9f0484769a363d1d6dc87f8885e99cac87327c6a5f60fb34580020a49129"},{"label":"foundry_sdk.v2.filesystem.models.FolderRid","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\filesystem\\models\\FolderRid.md","exists":true,"sha256":"dc80c8e77a2660742e20098a3d9170f1c125cd33f4b98bbced4ccafd442843cd"},{"label":"foundry_sdk.v2.filesystem.models.ResourceDisplayName","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v2\\filesystem\\models\\ResourceDisplayName.md","exists":true,"sha256":"2839c930e7660f94316d47974b2e9817b975c0d6b055af9d585eaa869b0f8b6e"}]}
Actual assertion rows: [{"case_id":"F074-25","check":"success_typed","result":"PASS","requests":1},{"case_id":"F074-25","check":"success_raw_closed","result":"PASS","requests":1},{"case_id":"F074-25","check":"async_typed","result":"PASS","requests":1},{"case_id":"F074-25","check":"async_raw_closed","result":"PASS","requests":1},{"case_id":"F074-25","check":"sync_stream_closed","result":"PASS","requests":1},{"case_id":"F074-25","check":"async_stream_closed","result":"PASS","requests":1},{"case_id":"F074-25","check":"error_BranchAlreadyExists","result":"PASS","status":409,"requests":1},{"case_id":"F074-25","check":"error_CreateBranchPermissionDenied","result":"PASS","status":403,"requests":1},{"case_id":"F074-25","check":"error_CreateDatasetPermissionDenied","result":"PASS","status":403,"requests":1},{"case_id":"F074-25","check":"error_DatasetNotFound","result":"PASS","status":404,"requests":1},{"case_id":"F074-25","check":"error_FolderNotFound","result":"PASS","status":404,"requests":1},{"case_id":"F074-25","check":"error_InvalidBranchName","result":"PASS","status":400,"requests":1},{"case_id":"F074-25","check":"error_InvalidDisplayName","result":"PASS","status":400,"requests":1},{"case_id":"F074-25","check":"error_ResourceNameAlreadyExists","result":"PASS","status":409,"requests":1},{"case_id":"F074-25","check":"error_TransactionNotCommitted","result":"PASS","status":400,"requests":1},{"case_id":"F074-25","check":"error_TransactionNotFound","result":"PASS","status":404,"requests":1},{"case_id":"F074-25","check":"error_IndependentPermissionDenied","result":"PASS","status":401,"requests":1},{"case_id":"F074-25","check":"error_IndependentPermissionDenied","result":"PASS","status":403,"requests":1},{"case_id":"F074-25","check":"timeout_no_retry","result":"PASS","requests":1},{"case_id":"F074-25","check":"malformed_json","result":"PASS"},{"case_id":"F074-25","check":"missing_required_name","result":"PASS","requests":0},{"case_id":"F074-25","check":"missing_required_parent_folder_rid","result":"PASS","requests":0},{"case_id":"F074-25","check":"optional omission_typed","result":"PASS","requests":1},{"case_id":"F074-25","check":"optional omission_raw_closed","result":"PASS","requests":1},{"case_id":"F074-25","check":"required argument omitted","result":"PASS","requests":0}]
Offline serializer, typed/raw/stream/error and bounded control-flow evidence. Tenant effects and integrated J12 remain outside this execution.
