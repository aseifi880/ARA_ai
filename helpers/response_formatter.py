def sanitize(list_of_objs):
    """
    receives a list of dicts that might belong to either a job or resume instance,
    which are obtained from their get methods (service.get_jobs, service.get_resumes) .
    returns a sanitized list for display purpose only
    """
    sanitized = []
    for c in list_of_objs:
        content = c.get("content", {})
        src = c.get("source_url")
        fetched_at = c.get("fetched_at")
        fetched_at_iso = fetched_at.isoformat() if fetched_at else None
        sanitized.append({
            "source_url": src,
            "fetched_at": fetched_at_iso,
            "content": content
        })
    return sanitized
