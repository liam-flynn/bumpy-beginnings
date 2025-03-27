def get_breadcrumbs(request):
    # get the url path and split it into an array
    path_parts = request.path.strip('/').split('/')
    # all breadcrumbs start with home
    breadcrumbs = [("Home", "/")]

    # "Forum" breadcrumbs
    if path_parts and path_parts[0] == "forums":
        breadcrumbs.append(("Forums", "/forums/"))
        # For forum detail pages like /forums/1/
        if len(path_parts) >= 2:
            if path_parts[1] == "new":
                breadcrumbs.append(("Create New Forum", "/forums/new"))
            else:
                breadcrumbs.append(("Forum Posts", f"/forums/{path_parts[1]}"))
            if len(path_parts) == 4 and path_parts[3].isdigit():
                breadcrumbs.append(
                    ("Post Page", f"/forums/{path_parts[1]}/posts/{path_parts[3]}"))

    # "Calculator" breadcrumbs
    if path_parts and path_parts[0] == "calculator":
        breadcrumbs.append(("Benefit Calculator", "/calculator/"))
        if len(path_parts) == 2 and path_parts[1] == "benefit-list":
            breadcrumbs.append(("Manage Benefits", "/calculator/benefit-list"))

    # "Article" breadcrumbs
    if path_parts and path_parts[0] == "articles":
        if request.user.is_staff:
            breadcrumbs.append(("Manage Articles", "/articles/"))
            if len(path_parts) == 2 and path_parts[1] == "new":
                breadcrumbs.append(("Create New Article", None))
        if len(path_parts) >= 3 and path_parts[2] == "view":
            breadcrumbs.append(("View Article", None))
        elif len(path_parts) >= 3 and path_parts[2] == "edit":
            breadcrumbs.append(("Edit Article", None))

    # "Milestone tracker" breadcrumbs
    if path_parts and path_parts[0] == "tracker":
        breadcrumbs.append(("Development Tracker Management", "/tracker/"))
        if len(path_parts) == 2 and path_parts[1] == "new":
            breadcrumbs.append(("Create New Milestone", None))
        if len(path_parts) >= 3:
            if path_parts[2] == "view":
                breadcrumbs.append(("View Milestone", None))
            elif path_parts[2] == "edit":
                breadcrumbs.append(("Edit Milestone", None))

    return breadcrumbs
