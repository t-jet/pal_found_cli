

# ── Build-queue sub-handler ─────────────────────────────────────────────────

def _handle_build_queue(
    args: argparse.Namespace,
    bq_parser: argparse.ArgumentParser,
) -> None:
    """Dispatch build-queue subcommands."""
    if not args.build_queue_command:
        bq_parser.print_help()
        raise ValidationError("build-queue subcommand required")
    
    from tracker.build_queue import build_queue
    
    if args.build_queue_command == "stage1":
        tickets = build_queue("stage1")
        print(f"\nStage 1: {len(tickets)} non-terminal ticket(s)")
        for t in tickets:
            print(f"  {t['id']}: {t['title']} ({t['status']})")
    
    elif args.build_queue_command == "stage2":
        tickets = build_queue("stage2", author=args.author)
        print(f"\nStage 2: {len(tickets)} tickets after priority reconciliation")
        for t in tickets:
            print(f"  {t['id']}: {t['title']} (priority={t['priority']})")
    
    elif args.build_queue_command == "stage3":
        tickets = build_queue("stage3", author=args.author)
        print(f"\nStage 3: {len(tickets)} tickets after sorting")
        print(f"\n{'#':<4} {'ID':<15} {'Priority':<8} {'Title':<40}")
        print("-" * 70)
        for pos, t in enumerate(tickets, 1):
            print(f"{pos:<4} {t['id']:<15} {t['priority']:<8} {t['title']:<40}")
    
    elif args.build_queue_command == "stage4":
        tickets = build_queue("stage4", author=args.author)
        print(f"\nBuild Queue (with blocking relationships):")
        print("=" * 100)
        for pos, t in enumerate(tickets, 1):
            priority_label = f"[{t['priority']}]"
            print(f"\n{pos}. {t['id']}: {t['title']}")
            print(f"   Priority: {priority_label} {t['priority_description']}")
            print(f"   Status: {t['status']}")
            if t.get('blocking'):
                print(f"   ⚠  BLOCKED by {len(t['blocking'])} ticket(s):")
                for blocker_id in t['blocking']:
                    blocker = next((bt for bt in tickets if bt['id'] == blocker_id), None)
                    if blocker:
                        print(f"      - {blocker_id}: {blocker['title']}")
            if t.get('blocking_me'):
                print(f"   ⏳ BLOCKS {len(t['blocking_me'])} ticket(s):")
                for blocked_id in t['blocking_me']:
                    blocked = next((bt for bt in tickets if bt['id'] == blocked_id), None)
                    if blocked:
                        print(f"      - {blocked_id}: {blocked['title']}")
    
    elif args.build_queue_command == "all":
        tickets = build_queue("all", author=args.author)
        print(f"\nBuild Queue (final): {len(tickets)} ticket(s)")
        print("=" * 100)
        for pos, t in enumerate(tickets, 1):
            priority_label = f"[{t['priority']}]"
            print(f"\n{pos}. {t['id']}: {t['title']}")
            print(f"   Priority: {priority_label} {t['priority_description']}")
            print(f"   Status: {t['status']}")
            if t.get('blocking'):
                print(f"   ⚠  Blocked by {len(t['blocking'])} ticket(s)")
            if t.get('blocking_me'):
                print(f"   ⏳ Blocks {len(t['blocking_me'])} ticket(s)")
    
    return EXIT_OK


# ── Parse & dispatch ─────────────────────────────────────────────────
args = parser.parse_args()

if args.help_toon:
    print(to_toon(_build_help_data()), end="")
    return EXIT_OK

if not args.command:
    return EXIT_OK

    cfg = get_runtime_config()

    if args.command == "create":
        validate_ticket_type(args.type)
        title = args.title_positional or args.title_opt
        if not title or not title.strip():
            create_p.error(
                "title is required: provide it as a positional argument "
                'or via --title "Your title here"'
            )
        description = decode_escape_sequences(args.description)
        if args.description_file:
            desc_path = Path(args.description_file)
            if not desc_path.exists():
                create_p.error(
                    f"--description-file not found: {args.description_file}"
                )
            try:
                description = desc_path.read_text(encoding="utf-8")
            except Exception as exc:
                create_p.error(
                    f"Failed to read --description-file "
                    f"'{args.description_file}': {exc}"
                )
        extras = parse_extra_fields(args.field)
        ticket_id = create_ticket(
            args.type, title, args.author,
            args.priority, args.assignee, args.parent,
            args.addressed_to, description, extras,
        )
        ticket = get_ticket(ticket_id)
        ctx = build_status_context(ticket_id, args.type, ticket["status"])
        print(yaml.dump(
            ctx, default_flow_style=False, allow_unicode=True,
            sort_keys=False,
        ))

    elif args.command == "get":
        ticket = get_ticket_with_content(args.ticket_id)
        ctx = build_status_context(
            ticket["id"], ticket["type"], ticket["status"],
        )
        print(yaml.dump(
            ctx, default_flow_style=False, allow_unicode=True,
            sort_keys=False,
        ))
        print("Ticket Details:")
        print("=" * 80)
        for key, value in ticket.items():
            if key == "content":
                continue
            print(f"{key:15s}: {value}")
        print("content:")
        print(ticket["content"])

    elif args.command == "list":
        if args.type:
            validate_ticket_type(args.type)
        if args.status:
            validate_status_value(args.status, args.type)
        if (
            args.priority
            and cfg["priority_values"]
            and args.priority not in cfg["priority_values"]
        ):
            raise ValidationError(
                f"Invalid priority filter: {args.priority}. "
                f"Valid values: {', '.join(cfg['priority_values'])}."
            )
        if args.parent:
            if not ticket_exists(args.parent):
                raise ValidationError(
                    f"Parent ticket {args.parent} does not exist"
                )
        tickets = list_tickets(
            args.status, args.assignee, args.type, args.priority,
            parent=args.parent,
            reporter=args.reporter,
        )
        print(f"\nFound {len(tickets)} ticket(s):")
        print("=" * 100)
        print(
            f"{'ID':<15} {'Status':<15} {'Priority':<10} "
            f"{'Assignee':<20} {'Title'}"
        )
        print("-" * 100)
        for t in tickets:
            print(format_ticket(t))

    elif args.command == "update":
        new_description: str | None = None
        if args.description:
            new_description = decode_escape_sequences(args.description)
        if args.description_file:
            desc_path = Path(args.description_file)
            if not desc_path.exists():
                update_p.error(
                    f"--description-file not found: {args.description_file}"
                )
            try:
                new_description = desc_path.read_text(encoding="utf-8")
            except Exception as exc:
                update_p.error(
                    f"Failed to read --description-file "
                    f"'{args.description_file}': {exc}"
                )
        update_extras: dict[str, str] | None = (
            parse_extra_fields(args.field) if args.field else None
        )
        ticket = update_ticket(
            args.ticket_id, args.author,
            args.status, args.assignee, args.priority,
            extra_fields=update_extras,
            description=new_description,
        )
        if args.status:
            ctx = build_status_context(
                ticket["id"], ticket["type"], ticket["status"],
            )
            print(yaml.dump(
                ctx, default_flow_style=False, allow_unicode=True,
                sort_keys=False,
            ))
        else:
            print(f"Updated ticket: {ticket['id']}")
            print(format_ticket(ticket))

    elif args.command == "link":
        if not args.link_command:
            link_p.print_help()
            return EXIT_VALIDATION_ERROR
        if args.link_command == "create":
            validate_link_type(args.link_type)
            lid = create_link(
                args.source_id, args.target_id, args.link_type,
                args.author, args.comment,
            )
            print(f"Created link: {lid}")
        elif args.link_command == "list":
            links = list_links(args.ticket_id, args.direction)
            print(f"\nFound {len(links)} link(s) for {args.ticket_id}:")
            print("=" * 100)
            print(
                f"{'Link ID':<15} {'Source':<15}    "
                f"{'Target':<15} {'Type':<15} {'Role'}"
            )
            print("-" * 100)
            for lk in links:
                print(format_link(lk))
        elif args.link_command == "remove":
            remove_link(args.link_id)
            print(f"Removed link: {args.link_id}")

    elif args.command == "comment":
        if not args.comment_command:
            comment_p.print_help()
            return EXIT_VALIDATION_ERROR
        if args.comment_command == "create":
            cid = create_comment(
                args.ticket_id, args.author, args.subject,
                decode_escape_sequences(args.text),
            )
            print(f"Created comment: {cid}")
        elif args.comment_command == "list":
            comments = list_comments(args.ticket_id)
            print(f"\nFound {len(comments)} comment(s) for {args.ticket_id}:")
            print("=" * 120)
            print(
                f"{'Comment ID':<30} {'Author':<20} "
                f"{'Created':<20} {'Updated':<20} {'Subject'}"
            )
            print("-" * 120)
            for c in comments:
                print(
                    f"{c['comment_id']:<30} {c['author']:<20} "
                    f"{c['created']:<20} {c['updated']:<20} {c['subject']}"
                )
        elif args.comment_command == "get":
            comment = get_comment(args.ticket_id, args.comment_id)
            print("\nComment Details:")
            print("=" * 80)
            print(f"comment_id      : {comment['comment_id']}")
            print(f"author          : {comment['author']}")
            print(f"subject         : {comment['subject']}")
            print(f"created         : {comment['created']}")
            print(f"updated         : {comment['updated']}")
            print("text:")
            print(comment["text"])
        elif args.comment_command == "update":
            if args.subject is None and args.text is None:
                raise ValidationError(
                    "Nothing to update. Fix: pass --subject and/or --text"
                )
            decoded_text = (
                decode_escape_sequences(args.text)
                if args.text is not None
                else None
            )
            updated = update_comment(
                args.ticket_id, args.comment_id, args.author,
                args.subject, decoded_text,
            )
            print(f"Updated comment: {updated['comment_id']}")

    elif args.command == "search":
        tickets = search_tickets(
            args.query, args.in_title, args.in_content,
        )
        print(f"\nFound {len(tickets)} ticket(s) matching '{args.query}':")
        print("=" * 100)
        print(
            f"{'ID':<15} {'Status':<15} {'Priority':<10} "
            f"{'Assignee':<20} {'Title'}"
        )
        print("-" * 100)
        for t in tickets:
            print(format_ticket(t))

    elif args.command == "type-info":
        validate_ticket_type(args.ticket_type)
        paths = get_paths()
        # Find the $ref path for this ticket type in the raw workflow file
        with open(paths.workflow_file, "r", encoding="utf-8") as _wf:
            raw_workflow = yaml.safe_load(_wf) or {}
        ref_file: Path | None = None
        for _entry in raw_workflow.get("ticket_types", []):
            if not isinstance(_entry, dict):
                continue
            _ref = _entry.get("$ref")
            if _ref:
                _candidate = paths.config_dir / _ref
                try:
                    with open(_candidate, "r", encoding="utf-8") as _tf:
                        _loaded = yaml.safe_load(_tf)
                    if isinstance(_loaded, dict) and _loaded.get("type") == args.ticket_type:
                        ref_file = _candidate
                        break
                except Exception:
                    continue
        if ref_file is None:
            raise ConfigurationError(
                f"No configuration file found for ticket type '{args.ticket_type}'. "
                "Fix: ensure the type has a $ref entry in ticket_types in .workflow.yaml"
            )
        print(ref_file.read_text(encoding="utf-8"), end="")

    elif args.command == "workflow":
        _handle_workflow(args, cfg, wf_p)

    return EXIT_OK

except FileOperationError as e:
    print(f"FileOperationError [{EXIT_FILE_ERROR}]: {e}")
    return EXIT_FILE_ERROR
except ConfigurationError as e:
    print(f"ConfigurationError [{EXIT_CONFIG_ERROR}]: {e}")
    return EXIT_CONFIG_ERROR
except TrackerError as e:
    print(f"ValidationError [{EXIT_VALIDATION_ERROR}]: {e}")
    return EXIT_VALIDATION_ERROR
except Exception as e:
    print(f"UnexpectedError [{EXIT_UNEXPECTED_ERROR}]: {e}")
    return EXIT_UNEXPECTED_ERROR
