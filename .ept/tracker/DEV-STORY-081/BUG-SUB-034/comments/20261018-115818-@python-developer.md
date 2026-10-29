Subject: Root cause and fix plan
Created: 2026-10-18T11:58:18
Updated: 2026-10-18T11:58:18
---
Scope: correct SUCCESS payloads in two OntologyScenario REST-081 examples. SDK 1.101.0 model docstrings for ListScenarioEditedObjectsResponse, LinksFromObject, and LinkedObjectLocator say edited object responses contain locator-only `__primaryKey` and `__apiName`. Current mocked responses used full Order/Worker domain properties, so the scripts passed while teaching the wrong response contract.
Plan: replace only those payloads with Order/Worker locators; keep the request and decoded-response assertions; run each offline fixture and REST acceptance tests; publish commit for independent semantic QA. No live service or application log exists for these offline examples; fixture stdout and test result will be recorded here.
