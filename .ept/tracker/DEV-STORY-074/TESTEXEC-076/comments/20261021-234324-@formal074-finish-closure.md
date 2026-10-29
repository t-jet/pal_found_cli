Subject: F074-17 real formal PASS v1.datasets.Transaction.commit
Created: 2026-10-21T23:43:24
Updated: 2026-10-21T23:43:24
---
Actual independent executor /root/formal074_prepare/independent_execute. Recorded by /root/formal074_finish_closure. v1.datasets.Transaction.commit
Actual run 2026-10-21T12:48:52.893101+00:00 to 2026-10-21T12:48:54.357938+00:00; exit 0. Cases SHA256 599ee752c7c375d5afca7b12620527f74734f9e053f4e4c0060f3b6ecdfb6632; harness SHA256 ff6a8c6d15d25225c1c3a74755f73c7494011967968b652430d36a5a9ed72d05. SDK 1.101.0 source/module/method and current asset hashes match approved oracle.
Fresh httpx.MockTransport, fake independent-qa-074 credential, literal requests/results/errors. Socket connect/connect_ex/create_connection and DNS denied; explicit denial probes passed. Logs .ept/tmp/rest074_formal_execute.log SHA256 d4f695b522147d12976aaf2f2b41641d9eec1be26ecf185ae949ec1623e0e04c; full result JSON SHA256 a5052af29a75e92f3b5dbc2e13b0476a12c399eac492efddfff871c4c2892613.
Actual local discovery: {"case_id":"F074-17","operation":"v1.datasets.Transaction.commit","checks":{"catalog_service_link":true,"index_exact_operation_contract":true,"contract_operation_heading":true,"contract_resource_guide_link":true,"behavior_method_heading":true,"behavior_example_link":true,"contract_model_definitions_resolve":true,"all_contract_local_links_resolve":true,"bound_asset_hashes":true},"catalog":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\catalog.md","sha256":"a2640d2c28ce15c8186af7c4525615a7cca32186783ca4079be0ed2424f492a7"},"index":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\v1\\datasets\\index.md","sha256":"559f526c22d5aeafdede99f095e8a98d34023f78b38e6d0c57aed4968af488f3"},"contract":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\contracts\\v1\\datasets\\Transaction\\commit.md","sha256":"4714419dbd559389f50b912abf5e9382985ed252ebd369f74e44097d127bdb9b","heading":"# v1.datasets.Transaction.commit"},"behavior":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\v1\\datasets\\Transaction.md","sha256":"5c77e19095a5cd10388035f010c958b00158dbb0b0397421303bb00c37e07a29","heading":"### commit"},"example":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\\examples\
est\\074\\v1\\datasets\\Transaction\\commit.py","sha256":"c4f3e96546b74ecae7cc953762b0aafb8cafced631397f5b23bd3e272bbfc4d7"},"model_links":[{"label":"foundry_sdk._core.api_client.ResponseMode","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\ResponseMode.md","exists":true,"sha256":"cbc428d84d3ac081d7cb101d8ee383fdbfd9ed09dd938608c91ac3c8e269f35f"},{"label":"foundry_sdk._core.api_client.SdkInternal","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\SdkInternal.md","exists":true,"sha256":"c2b86183f885c076f0c3c8b9a7f190b89a97e92ddeef26ddd57db3d1ed1fa4ca"},{"label":"foundry_sdk._core.model_base.ModelBase","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\ModelBase.md","exists":true,"sha256":"5f5b16aa4764220b3b6b9c4287c5bb45e46b9cbe122d8965f7a6461b0e030587"},{"label":"foundry_sdk._core.utils.AwareDatetime","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\AwareDatetime.md","exists":true,"sha256":"cb790e832ad9c9da79d728855fa1eef3ad96bfdc2862da210fb943c7a3f370e1"},{"label":"foundry_sdk._core.utils.RID","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\RID.md","exists":true,"sha256":"4af4eece28f34252abed320880118190a42c5cba5e72c27cd8dc8b72ecc223e2"},{"label":"foundry_sdk._core.utils.Timeout","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\Timeout.md","exists":true,"sha256":"1cd0a400d159d244916c364afaf160a1074016e2207d6bdd89e57f4292b3525a"},{"label":"foundry_sdk.v1.datasets.errors.CommitTransactionPermissionDenied","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\CommitTransactionPermissionDenied.md","exists":true,"sha256":"ad9d53c4b6f0d52b783f64adb06a5dedfbd249f5dbb0b9a924599f65c6e26380"},{"label":"foundry_sdk.v1.datasets.errors.CommitTransactionPermissionDeniedParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\CommitTransactionPermissionDeniedParameters.md","exists":true,"sha256":"45a843891c17c3e41dd5b3578c95f5087299d3e08356de08bb654b3637747c09"},{"label":"foundry_sdk.v1.datasets.errors.DatasetNotFound","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\DatasetNotFound.md","exists":true,"sha256":"675645f37e488c5609ac1f1c9343745130f7be9b1823301eddf250021ee51c95"},{"label":"foundry_sdk.v1.datasets.errors.DatasetNotFoundParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\DatasetNotFoundParameters.md","exists":true,"sha256":"8a10c7f77e7d5db9e8efc93ca0177311132451cbb755db5f60b06d02ef9d1f26"},{"label":"foundry_sdk.v1.datasets.errors.TransactionNotFound","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\TransactionNotFound.md","exists":true,"sha256":"757e509d474fc04e9d0b9b868821606800892e0a259361cfcca667af4c41f7a8"},{"label":"foundry_sdk.v1.datasets.errors.TransactionNotFoundParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\TransactionNotFoundParameters.md","exists":true,"sha256":"38bf34cb3b6eb59a44e489dd8e837db1c7220ba30e850d2afa3d90dcf3e3dc98"},{"label":"foundry_sdk.v1.datasets.errors.TransactionNotOpen","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\TransactionNotOpen.md","exists":true,"sha256":"ce5e2cd0ecc228b6170715c09d353e05fcd50a787fbf8d8a9164c4fd154c8945"},{"label":"foundry_sdk.v1.datasets.errors.TransactionNotOpenParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\TransactionNotOpenParameters.md","exists":true,"sha256":"08a91d0198df47679a5db5ee007185f966ea6766d05cceba9b7b0108793db07a"},{"label":"foundry_sdk.v1.datasets.models.DatasetRid","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\models\\DatasetRid.md","exists":true,"sha256":"31c5609cfff2d2d6a72113faf6fe0519648b43b3ac42f3f38e1f8ed630f680c2"},{"label":"foundry_sdk.v1.datasets.models.Transaction","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\models\\Transaction.md","exists":true,"sha256":"bf46a83f2bdfbf607e2bc19841128a195efbe3035f0b6120aae1f2c925b34375"},{"label":"foundry_sdk.v1.datasets.models.TransactionRid","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\models\\TransactionRid.md","exists":true,"sha256":"b77855a6ab9595d0ea97c6fd304e3f9eb54ad1ec86881957255e7993d715474c"},{"label":"foundry_sdk.v1.datasets.models.TransactionStatus","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\models\\TransactionStatus.md","exists":true,"sha256":"e73a88842a694047f3156e425d1f0a06cce800f3d00469f6972dbed108b664e3"},{"label":"foundry_sdk.v1.datasets.models.TransactionType","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\models\\TransactionType.md","exists":true,"sha256":"1d482c740d96d0c8b29dc24ebee594c6490d985b9de70af553e0808989f3cfe9"}]}
Actual assertion rows: [{"case_id":"F074-17","check":"success_typed","result":"PASS","requests":1},{"case_id":"F074-17","check":"success_raw_closed","result":"PASS","requests":1},{"case_id":"F074-17","check":"async_typed","result":"PASS","requests":1},{"case_id":"F074-17","check":"async_raw_closed","result":"PASS","requests":1},{"case_id":"F074-17","check":"sync_stream_closed","result":"PASS","requests":1},{"case_id":"F074-17","check":"async_stream_closed","result":"PASS","requests":1},{"case_id":"F074-17","check":"error_CommitTransactionPermissionDenied","result":"PASS","status":403,"requests":1},{"case_id":"F074-17","check":"error_DatasetNotFound","result":"PASS","status":404,"requests":1},{"case_id":"F074-17","check":"error_TransactionNotFound","result":"PASS","status":404,"requests":1},{"case_id":"F074-17","check":"error_TransactionNotOpen","result":"PASS","status":400,"requests":1},{"case_id":"F074-17","check":"error_IndependentPermissionDenied","result":"PASS","status":401,"requests":1},{"case_id":"F074-17","check":"error_IndependentPermissionDenied","result":"PASS","status":403,"requests":1},{"case_id":"F074-17","check":"timeout_no_retry","result":"PASS","requests":1},{"case_id":"F074-17","check":"malformed_json","result":"PASS"},{"case_id":"F074-17","check":"missing_required_dataset_rid","result":"PASS","requests":0},{"case_id":"F074-17","check":"missing_required_transaction_rid","result":"PASS","requests":0},{"case_id":"F074-17","check":"optional omission_typed","result":"PASS","requests":1},{"case_id":"F074-17","check":"optional omission_raw_closed","result":"PASS","requests":1},{"case_id":"F074-17","check":"required argument omitted","result":"PASS","requests":0}]
Offline serializer, typed/raw/stream/error and bounded control-flow evidence. Tenant effects and integrated J12 remain outside this execution.
