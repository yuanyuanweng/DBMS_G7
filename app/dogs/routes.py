'''
Dog-related routes.

This file handles dog-related pages and API endpoints, such as:
- viewing all dogs (Page rendering)
- viewing one dog's detail page (Page rendering)
- providing dog data for the frontend (API routes)

=== Wikipedia? ===
1)Page rendering
Flask directly returns an HTML template.
Example: /dogs → render_template("dogs/list.html", dogs=dogs)

2)API routes
Flask returns data, usually JSON, for JavaScript/frontend to use.
Example: /api/dogs → jsonify(dogs)


TODO:
Before the database schema is ready:
- Define basic API routes.
- Use mock dog data for testing.
- Make sure frontend pages can receive and display dog data.

After the database schema is ready:
- Import the Dog model from app/models.
- Replace mock data with real database queries.
- Add filtering/search logic based on request parameters.
- Add create/edit/delete routes if needed.
'''
