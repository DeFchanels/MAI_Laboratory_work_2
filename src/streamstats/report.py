import json


def make_report(events_count, levels_counters, sources_counters, top_errors_counters, first_timestamp, last_timestamp, invalid_skips, output_path='report.json'):
    result = {
        "total_events": events_count,
        "levels_counters": levels_counters,
        "sources_counters": sources_counters,
        "top_errors_sources": top_errors_counters,
        "first_timestamp": first_timestamp,
        "last_timestamp": last_timestamp,
        "invalid_events_skipped": invalid_skips
    }
    with open(output_path, 'w') as f:
        json.dump(result, f, indent=4)

