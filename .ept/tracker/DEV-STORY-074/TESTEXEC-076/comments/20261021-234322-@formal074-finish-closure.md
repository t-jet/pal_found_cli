Subject: F074-10 real formal PASS v1.datasets.Dataset.replace_schema
Created: 2026-10-21T23:43:22
Updated: 2026-10-21T23:43:22
---
Actual independent executor /root/formal074_prepare/independent_execute. Recorded by /root/formal074_finish_closure. v1.datasets.Dataset.replace_schema
Actual run 2026-10-21T12:48:52.893101+00:00 to 2026-10-21T12:48:54.357938+00:00; exit 0. Cases SHA256 599ee752c7c375d5afca7b12620527f74734f9e053f4e4c0060f3b6ecdfb6632; harness SHA256 ff6a8c6d15d25225c1c3a74755f73c7494011967968b652430d36a5a9ed72d05. SDK 1.101.0 source/module/method and current asset hashes match approved oracle.
Fresh httpx.MockTransport, fake independent-qa-074 credential, literal requests/results/errors. Socket connect/connect_ex/create_connection and DNS denied; explicit denial probes passed. Logs .ept/tmp/rest074_formal_execute.log SHA256 d4f695b522147d12976aaf2f2b41641d9eec1be26ecf185ae949ec1623e0e04c; full result JSON SHA256 a5052af29a75e92f3b5dbc2e13b0476a12c399eac492efddfff871c4c2892613.
Actual local discovery: {"case_id":"F074-10","operation":"v1.datasets.Dataset.replace_schema","checks":{"catalog_service_link":true,"index_exact_operation_contract":true,"contract_operation_heading":true,"contract_resource_guide_link":true,"behavior_method_heading":true,"behavior_example_link":true,"contract_model_definitions_resolve":true,"all_contract_local_links_resolve":true,"bound_asset_hashes":true},"catalog":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\catalog.md","sha256":"a2640d2c28ce15c8186af7c4525615a7cca32186783ca4079be0ed2424f492a7"},"index":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\v1\\datasets\\index.md","sha256":"559f526c22d5aeafdede99f095e8a98d34023f78b38e6d0c57aed4968af488f3"},"contract":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\contracts\\v1\\datasets\\Dataset\
eplace_schema.md","sha256":"a59cfb46fa789864c1b382e071a20b25d786060be860680c4032b7904c79d5f1","heading":"# v1.datasets.Dataset.replace_schema"},"behavior":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\v1\\datasets\\Dataset.md","sha256":"3a0ada9932bd0b06b615df992f8a2cd95898bec036fdfd416f4302396a509d45","heading":"### replace_schema"},"example":{"path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\\examples\
est\\074\\v1\\datasets\\Dataset\
eplace_schema.py","sha256":"727ea58f48c027f80e8057448135972674a684eeb990d48bf1e1d4cee6b748c6"},"model_links":[{"label":"foundry_sdk._core.api_client.ResponseMode","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\ResponseMode.md","exists":true,"sha256":"cbc428d84d3ac081d7cb101d8ee383fdbfd9ed09dd938608c91ac3c8e269f35f"},{"label":"foundry_sdk._core.api_client.SdkInternal","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\SdkInternal.md","exists":true,"sha256":"c2b86183f885c076f0c3c8b9a7f190b89a97e92ddeef26ddd57db3d1ed1fa4ca"},{"label":"foundry_sdk._core.utils.RID","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\RID.md","exists":true,"sha256":"4af4eece28f34252abed320880118190a42c5cba5e72c27cd8dc8b72ecc223e2"},{"label":"foundry_sdk._core.utils.Timeout","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\_core\\Timeout.md","exists":true,"sha256":"1cd0a400d159d244916c364afaf160a1074016e2207d6bdd89e57f4292b3525a"},{"label":"foundry_sdk.v1.core.models.FilePath","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\core\\models\\FilePath.md","exists":true,"sha256":"51e98cd7a06008abc58c0113c5797637995200192914c883c13de9ef53ab0be9"},{"label":"foundry_sdk.v1.core.models.PreviewMode","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\core\\models\\PreviewMode.md","exists":true,"sha256":"c18f504a80464947bd1105b8ec0c32afabc9711b88bec17e1d626c395c85ad6e"},{"label":"foundry_sdk.v1.datasets.errors.AbortTransactionPermissionDenied","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\AbortTransactionPermissionDenied.md","exists":true,"sha256":"bb2362f732ac081fe1f54fd6297c7f9d7c22346ced9f7aca3b8c31618519e9aa"},{"label":"foundry_sdk.v1.datasets.errors.AbortTransactionPermissionDeniedParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\AbortTransactionPermissionDeniedParameters.md","exists":true,"sha256":"8f573ab78a8580f3b90a49d6ba4ec7908c0eb9a059d906b8345a5fb7644325a5"},{"label":"foundry_sdk.v1.datasets.errors.BranchNotFound","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\BranchNotFound.md","exists":true,"sha256":"97855c730b4ff55ad277b6f32567a134c9d41013dba7f3572611941afa2d33ab"},{"label":"foundry_sdk.v1.datasets.errors.BranchNotFoundParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\BranchNotFoundParameters.md","exists":true,"sha256":"1a9cb75734453404a44e52d5132fc56582b3e4148a5bc07b4ae3e5767aac347c"},{"label":"foundry_sdk.v1.datasets.errors.CommitTransactionPermissionDenied","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\CommitTransactionPermissionDenied.md","exists":true,"sha256":"ad9d53c4b6f0d52b783f64adb06a5dedfbd249f5dbb0b9a924599f65c6e26380"},{"label":"foundry_sdk.v1.datasets.errors.CommitTransactionPermissionDeniedParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\CommitTransactionPermissionDeniedParameters.md","exists":true,"sha256":"45a843891c17c3e41dd5b3578c95f5087299d3e08356de08bb654b3637747c09"},{"label":"foundry_sdk.v1.datasets.errors.CreateTransactionPermissionDenied","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\CreateTransactionPermissionDenied.md","exists":true,"sha256":"b9e784e00e85a1051a4aea4b976a5759a822997202a2b62e9e6c6802bf6e481e"},{"label":"foundry_sdk.v1.datasets.errors.CreateTransactionPermissionDeniedParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\CreateTransactionPermissionDeniedParameters.md","exists":true,"sha256":"4640ef981c617a760530e8576667ac12333cbe3ed51acba0244d2584af4da572"},{"label":"foundry_sdk.v1.datasets.errors.DatasetNotFound","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\DatasetNotFound.md","exists":true,"sha256":"675645f37e488c5609ac1f1c9343745130f7be9b1823301eddf250021ee51c95"},{"label":"foundry_sdk.v1.datasets.errors.DatasetNotFoundParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\DatasetNotFoundParameters.md","exists":true,"sha256":"8a10c7f77e7d5db9e8efc93ca0177311132451cbb755db5f60b06d02ef9d1f26"},{"label":"foundry_sdk.v1.datasets.errors.FileNotFoundOnTransactionRange","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\FileNotFoundOnTransactionRange.md","exists":true,"sha256":"337e6b8b22daefda92da24bf7e2e4ace9f0a34c06e16e5eb54e70f798d773d78"},{"label":"foundry_sdk.v1.datasets.errors.FileNotFoundOnTransactionRangeParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\FileNotFoundOnTransactionRangeParameters.md","exists":true,"sha256":"9dc9049d00b1f5790fb9d6869230657fc812bbd74053edbef8a860e0fb3c12ad"},{"label":"foundry_sdk.v1.datasets.errors.InvalidBranchId","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\InvalidBranchId.md","exists":true,"sha256":"c39bcde108e62627a6ca3a35cbdb338d1cce6ccd9c0814ee5cfa77560945aba8"},{"label":"foundry_sdk.v1.datasets.errors.InvalidBranchIdParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\InvalidBranchIdParameters.md","exists":true,"sha256":"3470c031f0fb392703efd8a73fcada2989b8f228ac8d030f58bf9edd202880c3"},{"label":"foundry_sdk.v1.datasets.errors.InvalidTransactionType","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\InvalidTransactionType.md","exists":true,"sha256":"c34404e54bc089457e2e7677065028a9e68d162a9b3d62dc089612860558f69f"},{"label":"foundry_sdk.v1.datasets.errors.InvalidTransactionTypeParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\InvalidTransactionTypeParameters.md","exists":true,"sha256":"0f67ccfcc91ce9e912de893b2223f572f5f5a633a5abd853402ea9688f094478"},{"label":"foundry_sdk.v1.datasets.errors.OpenTransactionAlreadyExists","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\OpenTransactionAlreadyExists.md","exists":true,"sha256":"4e5aed67253212481dbdd98618ba1ba4e913e6a090755ab137030189771eef05"},{"label":"foundry_sdk.v1.datasets.errors.OpenTransactionAlreadyExistsParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\OpenTransactionAlreadyExistsParameters.md","exists":true,"sha256":"feb7948ee817b8f8a4a5e0e776c7c8a099ea708cb70218d9758fed92e9b500fc"},{"label":"foundry_sdk.v1.datasets.errors.PutSchemaPermissionDenied","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\PutSchemaPermissionDenied.md","exists":true,"sha256":"6a4f15af558569129f529706c2aa9d5f28ef7469f35fff65bed34203cd2ff4be"},{"label":"foundry_sdk.v1.datasets.errors.PutSchemaPermissionDeniedParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\PutSchemaPermissionDeniedParameters.md","exists":true,"sha256":"c21da1a965811f64f723daf32c77e5d6e41ca5a9eed4c5860354b3919ae03fa1"},{"label":"foundry_sdk.v1.datasets.errors.TransactionNotFound","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\TransactionNotFound.md","exists":true,"sha256":"757e509d474fc04e9d0b9b868821606800892e0a259361cfcca667af4c41f7a8"},{"label":"foundry_sdk.v1.datasets.errors.TransactionNotFoundParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\TransactionNotFoundParameters.md","exists":true,"sha256":"38bf34cb3b6eb59a44e489dd8e837db1c7220ba30e850d2afa3d90dcf3e3dc98"},{"label":"foundry_sdk.v1.datasets.errors.TransactionNotOpen","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\TransactionNotOpen.md","exists":true,"sha256":"ce5e2cd0ecc228b6170715c09d353e05fcd50a787fbf8d8a9164c4fd154c8945"},{"label":"foundry_sdk.v1.datasets.errors.TransactionNotOpenParameters","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\errors\\TransactionNotOpenParameters.md","exists":true,"sha256":"08a91d0198df47679a5db5ee007185f966ea6766d05cceba9b7b0108793db07a"},{"label":"foundry_sdk.v1.datasets.models.BranchId","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\models\\BranchId.md","exists":true,"sha256":"1e1d4b0aaa8f9e79865671f0df6791deda0dda20a0ca9fb973b01d9c420224d7"},{"label":"foundry_sdk.v1.datasets.models.DatasetRid","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\models\\DatasetRid.md","exists":true,"sha256":"31c5609cfff2d2d6a72113faf6fe0519648b43b3ac42f3f38e1f8ed630f680c2"},{"label":"foundry_sdk.v1.datasets.models.TransactionRid","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\models\\TransactionRid.md","exists":true,"sha256":"b77855a6ab9595d0ea97c6fd304e3f9eb54ad1ec86881957255e7993d715474c"},{"label":"foundry_sdk.v1.datasets.models.TransactionStatus","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\models\\TransactionStatus.md","exists":true,"sha256":"e73a88842a694047f3156e425d1f0a06cce800f3d00469f6972dbed108b664e3"},{"label":"foundry_sdk.v1.datasets.models.TransactionType","path":"E:\\learn\\GenAI_Foundations_DA\\git\\foundry_cli\\.ept\	mp\\feature015_integration\\.agents\\skills\\pal-found-dev\
eferences\
est\\models\\v1\\datasets\\models\\TransactionType.md","exists":true,"sha256":"1d482c740d96d0c8b29dc24ebee594c6490d985b9de70af553e0808989f3cfe9"}]}
Actual assertion rows: [{"case_id":"F074-10","check":"success_typed","result":"PASS","requests":1},{"case_id":"F074-10","check":"success_raw_closed","result":"PASS","requests":1},{"case_id":"F074-10","check":"async_typed","result":"PASS","requests":1},{"case_id":"F074-10","check":"async_raw_closed","result":"PASS","requests":1},{"case_id":"F074-10","check":"error_AbortTransactionPermissionDenied","result":"PASS","status":403,"requests":1},{"case_id":"F074-10","check":"error_BranchNotFound","result":"PASS","status":404,"requests":1},{"case_id":"F074-10","check":"error_CommitTransactionPermissionDenied","result":"PASS","status":403,"requests":1},{"case_id":"F074-10","check":"error_CreateTransactionPermissionDenied","result":"PASS","status":403,"requests":1},{"case_id":"F074-10","check":"error_DatasetNotFound","result":"PASS","status":404,"requests":1},{"case_id":"F074-10","check":"error_FileNotFoundOnTransactionRange","result":"PASS","status":404,"requests":1},{"case_id":"F074-10","check":"error_InvalidBranchId","result":"PASS","status":400,"requests":1},{"case_id":"F074-10","check":"error_InvalidTransactionType","result":"PASS","status":400,"requests":1},{"case_id":"F074-10","check":"error_OpenTransactionAlreadyExists","result":"PASS","status":409,"requests":1},{"case_id":"F074-10","check":"error_PutSchemaPermissionDenied","result":"PASS","status":403,"requests":1},{"case_id":"F074-10","check":"error_TransactionNotFound","result":"PASS","status":404,"requests":1},{"case_id":"F074-10","check":"error_TransactionNotOpen","result":"PASS","status":400,"requests":1},{"case_id":"F074-10","check":"error_IndependentPermissionDenied","result":"PASS","status":401,"requests":1},{"case_id":"F074-10","check":"error_IndependentPermissionDenied","result":"PASS","status":403,"requests":1},{"case_id":"F074-10","check":"timeout_no_retry","result":"PASS","requests":1},{"case_id":"F074-10","check":"missing_required_dataset_rid","result":"PASS","requests":0},{"case_id":"F074-10","check":"missing_required_body","result":"PASS","requests":0},{"case_id":"F074-10","check":"optional omission_typed","result":"PASS","requests":1},{"case_id":"F074-10","check":"optional omission_raw_closed","result":"PASS","requests":1},{"case_id":"F074-10","check":"required argument omitted","result":"PASS","requests":0}]
Offline serializer, typed/raw/stream/error and bounded control-flow evidence. Tenant effects and integrated J12 remain outside this execution.
