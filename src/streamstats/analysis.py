from streamstats.report import make_report


levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def analyser(events, skipped_events, output):
    events_count = len(events)
    if events_count:
        first_timestamp = min(event.timestamp for event in events).isoformat().replace("+00:00", "Z")
        last_timestamp = max(event.timestamp for event in events).isoformat().replace("+00:00", "Z")
        levels_counters = dict.fromkeys(levels, 0)
        sources_counters = dict.fromkeys([event.source for event in events], 0)
        top_errors_counters = dict.fromkeys([event.source for event in events], 0)
        for event in events:
            levels_counters[event.level] += 1
            sources_counters[event.source] += 1
            if event.level == "ERROR" or event.level == "CRITICAL":
                top_errors_counters[event.source] += 1
        top_5_errors_sources = dict(sorted(top_errors_counters.items(), key=lambda x: x[1], reverse=True)[:5])
        make_report(events_count + skipped_events, levels_counters, sources_counters, top_5_errors_sources, first_timestamp, last_timestamp, skipped_events, output)
    else:
        print("Files are empty or all events are invalid")
        make_report(skipped_events, 0, 0, 0, 0, 0, skipped_events, output)
