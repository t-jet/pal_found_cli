---
name: playwright-python
description: This skill equips an AI agent with the knowledge to write, debug, and reason about browser automation and end-to-end testing using **Playwright for Python**. The agent should consult the knowledge files below when answering questions, generating code, explaining concepts, or troubleshooting issues related to usage Playwright with Python 
license: MIT
metadata:
  version: "0.1.0"
---

# Playwright for Python Skill

## How to use this skill

1. Identify the user's intent (writing a test, understanding an API, debugging, CI setup, etc.).
2. Look up the relevant knowledge file(s) from the sections below.
3. Use the content of those files as authoritative reference when generating your response.
4. Prefer `core/` guides for conceptual and workflow questions; prefer `api/` references for method signatures, parameters, and class behaviour.

---

## Core Guides (`core/`)

Conceptual documentation, guides, and how-tos for working with Playwright.

| File | Summary |
|------|---------|
| [intro.mdx](core/intro.mdx) | Step-by-step installation guide for setting up Playwright and its browser binaries. |
| [writing-tests.mdx](core/writing-tests.mdx) | Explains the fundamental structure and conventions for authoring Playwright tests in Python. |
| [running-tests.mdx](core/running-tests.mdx) | Shows how to run, filter, and debug tests from the command line using the Playwright test runner. |
| [test-assertions.mdx](core/test-assertions.mdx) | Documents the built-in `expect` assertion API for validating page and element state in tests. |
| [locators.mdx](core/locators.mdx) | Covers Playwright's recommended locator strategies with auto-waiting and retry-ability. |
| [other-locators.mdx](core/other-locators.mdx) | Describes legacy and advanced locator types such as CSS, XPath, and text selectors. |
| [actionability.mdx](core/actionability.mdx) | Explains the auto-waiting mechanism that ensures elements are ready before actions are performed. |
| [pages.mdx](core/pages.mdx) | Describes the Page object lifecycle, multi-page scenarios, and popup handling. |
| [frames.mdx](core/frames.mdx) | Explains how to interact with iframes and nested frame trees within a page. |
| [navigations.mdx](core/navigations.mdx) | Covers page navigation methods, wait strategies, and handling redirects and load states. |
| [input.mdx](core/input.mdx) | Documents user-input actions including click, fill, select, drag-and-drop, and keyboard events. |
| [events.mdx](core/events.mdx) | Explains how to listen for and handle browser events such as requests, dialogs, and console messages. |
| [handles.mdx](core/handles.mdx) | Describes JSHandle and ElementHandle objects for holding references to in-page JavaScript values. |
| [evaluating.mdx](core/evaluating.mdx) | Shows how to execute JavaScript expressions in the browser context and retrieve their results. |
| [network.mdx](core/network.mdx) | Details network interception, request modification, response handling, and HAR recording. |
| [mock.mdx](core/mock.mdx) | Explains how to mock API responses and network requests to isolate tests from external services. |
| [api-testing.mdx](core/api-testing.mdx) | Guides standalone HTTP API testing using Playwright's `APIRequestContext` without a browser. |
| [auth.mdx](core/auth.mdx) | Covers authentication strategies including cookies, storage state, and reusing signed-in sessions. |
| [browser-contexts.mdx](core/browser-contexts.mdx) | Explains isolated browser contexts for independent sessions within a single browser instance. |
| [browsers.mdx](core/browsers.mdx) | Describes how to launch and configure Chromium, Firefox, and WebKit browser instances. |
| [emulation.mdx](core/emulation.mdx) | Shows how to emulate devices, viewports, geolocation, locale, timezone, and colour scheme. |
| [dialogs.mdx](core/dialogs.mdx) | Explains how to handle native browser dialogs such as alert, confirm, and prompt. |
| [downloads.mdx](core/downloads.mdx) | Covers intercepting and saving file downloads triggered by page interactions. |
| [screenshots.mdx](core/screenshots.mdx) | Documents page and element screenshot methods and options for visual capture. |
| [videos.mdx](core/videos.mdx) | Explains how to record video of browser sessions for debugging and documentation. |
| [trace-viewer-intro.mdx](core/trace-viewer-intro.mdx) | Introduction to the Playwright Trace Viewer tool for recording and replaying test traces. |
| [trace-viewer.mdx](core/trace-viewer.mdx) | Details Trace Viewer features including timeline, network panel, snapshots, and source view. |
| [pom.mdx](core/pom.mdx) | Demonstrates the Page Object Model pattern for organizing test code into reusable page classes. |
| [clock.mdx](core/clock.mdx) | Explains how to control and simulate browser time using the Clock API for time-dependent tests. |
| [aria-snapshots.mdx](core/aria-snapshots.mdx) | Covers ARIA snapshot testing for asserting the accessible structure of a page over time. |
| [debug.mdx](core/debug.mdx) | Describes tools and techniques for debugging Playwright scripts including the Inspector and verbose logs. |
| [codegen-intro.mdx](core/codegen-intro.mdx) | Introduction to the Playwright code generator for recording browser interactions as test code. |
| [codegen.mdx](core/codegen.mdx) | Full guide to using the interactive test generator UI, options, and selector configuration. |
| [service-workers.mdx](core/service-workers.mdx) | Explains how to intercept and handle service worker requests in browser contexts. |
| [touch-events.mdx](core/touch-events.mdx) | Covers simulation of touch gestures and multi-touch interactions for mobile testing. |
| [extensibility.mdx](core/extensibility.mdx) | Shows how to register custom selector engines to extend Playwright's built-in locator strategies. |
| [library.mdx](core/library.mdx) | Getting-started guide for using Playwright as a standalone library without the test runner. |
| [handles.mdx](core/handles.mdx) | Describes JSHandle and ElementHandle for holding references to JavaScript objects in the page. |
| [chrome-extensions.mdx](core/chrome-extensions.mdx) | Explains how to load and test Chrome browser extensions in a persistent context. |
| [selenium-grid.mdx](core/selenium-grid.mdx) | Describes experimental support for connecting Playwright to a Selenium Grid infrastructure. |
| [docker.mdx](core/docker.mdx) | Guide to running Playwright tests inside Docker containers with the official images. |
| [ci-intro.mdx](core/ci-intro.mdx) | Introduction to configuring CI pipelines to run Playwright tests automatically. |
| [ci.mdx](core/ci.mdx) | Detailed CI setup instructions for GitHub Actions, Azure Pipelines, GitLab CI, and others. |
| [webview2.mdx](core/webview2.mdx) | Explains how to automate Electron and WebView2 applications using Playwright. |
| [getting-started-cli.mdx](core/getting-started-cli.mdx) | Guide for using Playwright as a coding agent tool via the CLI interface. |
| [getting-started-mcp.mdx](core/getting-started-mcp.mdx) | Explains how to integrate Playwright as an MCP (Model Context Protocol) tool for AI agents. |
| [test-runners.mdx](core/test-runners.mdx) | Covers integrating Playwright with third-party test runners such as pytest and unittest. |
| [languages.mdx](core/languages.mdx) | Lists all programming languages supported by Playwright and links to their documentation. |
| [release-notes.mdx](core/release-notes.mdx) | Chronological changelog of Playwright releases with new features, fixes, and breaking changes. |

---

## API Reference (`api/`)

Class-level API documentation for all Playwright Python objects.

| File | Summary |
|------|---------|
| [class-playwright.mdx](api/class-playwright.mdx) | The root `Playwright` class that exposes browser types and the request context factory. |
| [class-browser.mdx](api/class-browser.mdx) | Represents a browser instance launched by Playwright, used to create contexts and pages. |
| [class-browsercontext.mdx](api/class-browsercontext.mdx) | An isolated browser session with its own cookies, storage, and network settings. |
| [class-browsertype.mdx](api/class-browsertype.mdx) | Provides methods to launch or connect to a specific browser (Chromium, Firefox, WebKit). |
| [class-page.mdx](api/class-page.mdx) | The central object for interacting with a single browser tab — navigation, actions, and events. |
| [class-frame.mdx](api/class-frame.mdx) | Represents a frame within a page, exposing the same interaction methods as `Page`. |
| [class-framelocator.mdx](api/class-framelocator.mdx) | A scoped locator that targets elements inside an `<iframe>` element. |
| [class-locator.mdx](api/class-locator.mdx) | The primary element-finding abstraction with built-in auto-waiting and retry logic. |
| [class-locatorassertions.mdx](api/class-locatorassertions.mdx) | Assertion methods for verifying the state, text, and attributes of a located element. |
| [class-pageassertions.mdx](api/class-pageassertions.mdx) | Assertion methods for verifying page-level state such as URL and title. |
| [class-apirequest.mdx](api/class-apirequest.mdx) | Factory class for creating `APIRequestContext` instances used for HTTP API testing. |
| [class-apirequestcontext.mdx](api/class-apirequestcontext.mdx) | Provides HTTP methods (GET, POST, PUT, DELETE, etc.) for making direct API calls in tests. |
| [class-apiresponse.mdx](api/class-apiresponse.mdx) | Represents the HTTP response returned by an `APIRequestContext` request method. |
| [class-apiresponseassertions.mdx](api/class-apiresponseassertions.mdx) | Assertion methods for verifying the status, headers, and body of an API response. |
| [class-request.mdx](api/class-request.mdx) | Represents a network request made by the page, exposing URL, method, headers, and body. |
| [class-response.mdx](api/class-response.mdx) | Represents a network response received by the page, exposing status, headers, and body. |
| [class-route.mdx](api/class-route.mdx) | Allows intercepting and fulfilling or aborting network requests matched by a route pattern. |
| [class-websocket.mdx](api/class-websocket.mdx) | Represents a WebSocket connection from the page, exposing send and received frames. |
| [class-websocketroute.mdx](api/class-websocketroute.mdx) | Allows intercepting and handling WebSocket connections similarly to HTTP route handling. |
| [class-elementhandle.mdx](api/class-elementhandle.mdx) | A handle to a DOM element in the page, providing lower-level interaction methods (prefer `Locator`). |
| [class-jshandle.mdx](api/class-jshandle.mdx) | Represents a JavaScript object inside the browser, returned by `evaluate_handle()`. |
| [class-keyboard.mdx](api/class-keyboard.mdx) | Low-level keyboard API for pressing individual keys, key combinations, and typing text. |
| [class-mouse.mdx](api/class-mouse.mdx) | Low-level mouse API for moving the pointer and dispatching click, down, and up events. |
| [class-touchscreen.mdx](api/class-touchscreen.mdx) | Low-level touchscreen API for dispatching touch tap events in touch-enabled browser contexts. |
| [class-clock.mdx](api/class-clock.mdx) | API for freezing, advancing, and mocking browser time to test time-sensitive application logic. |
| [class-dialog.mdx](api/class-dialog.mdx) | Represents a browser dialog (alert, confirm, prompt) dispatched via the `page.on("dialog")` event. |
| [class-download.mdx](api/class-download.mdx) | Represents a file download initiated by the page, with methods to access and save the content. |
| [class-filechooser.mdx](api/class-filechooser.mdx) | Represents a native file picker dialog, allowing tests to set files without OS interaction. |
| [class-consolemessage.mdx](api/class-consolemessage.mdx) | Represents a message logged to the browser console, including type, text, and location. |
| [class-worker.mdx](api/class-worker.mdx) | Represents a Web Worker or Service Worker running in the page context. |
| [class-cdpsession.mdx](api/class-cdpsession.mdx) | A raw Chrome DevTools Protocol session for advanced, low-level browser instrumentation. |
| [class-tracing.mdx](api/class-tracing.mdx) | API for starting, stopping, and exporting Playwright trace recordings for post-run analysis. |
| [class-video.mdx](api/class-video.mdx) | Represents a recorded video of a browser context page, with a method to retrieve the file path. |
| [class-screencast.mdx](api/class-screencast.mdx) | Interface for capturing individual screencast frames from a page programmatically. |
| [class-selectors.mdx](api/class-selectors.mdx) | API for registering custom selector engines to extend Playwright's element-finding capabilities. |
| [class-debugger.mdx](api/class-debugger.mdx) | API for controlling the Playwright Inspector debugger — pausing and resuming script execution. |
| [class-weberror.mdx](api/class-weberror.mdx) | Represents an unhandled JavaScript exception thrown in the page, dispatched as a context event. |
| [class-timeouterror.mdx](api/class-timeouterror.mdx) | Error subclass thrown when a Playwright action or assertion exceeds its configured timeout. |
| [class-error.mdx](api/class-error.mdx) | Base error class for Playwright-specific exceptions raised during automation. |
