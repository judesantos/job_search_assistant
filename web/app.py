import os
import json

from flask import Flask, request, render_template, redirect, url_for

from src.services.search_jobs import SearchJobs
from src.utils.parser import process_file

# Create a Flask application
app = Flask(__name__)

PAGE_INDEX_HTML = "index.html"
PAGE_RESULT_HTML = "results.html"


@app.route("/", methods=["GET", "POST"])
def home():
    """
    Home page route.
    Handles file upload and job search.
    Returns:
        Rendered HTML template with upload form and search input.
        If POST request, processes the uploaded file and performs job search.
    """
    if request.method == "POST":

        # ******************************
        # Validation
        # ******************************

        # Check if a file was uploaded
        if "file" not in request.files:
            error = "No file uploaded"
            return render_template(PAGE_INDEX_HTML, error=error)

        file = request.files["file"]
        # Check if the file is empty
        if file.filename == "":
            error = "No file selected"
            return render_template(PAGE_INDEX_HTML, error=error)

        # Get job keywords and location from the form
        keywords = request.form.get("keywords")
        if not keywords or keywords == "":
            error = "Keywords are required"
            return render_template(PAGE_INDEX_HTML, error=error)

        location = request.form.get("location")
        if not location or location == "":
            error = "Location is required"
            return render_template(PAGE_INDEX_HTML, error=error)

        # ******************************
        # Upload and read file
        # ******************************

        # Check the destination folder if file already exists
        # If not, process the file
        filename = f'{os.path.basename(file.filename)}.txt'
        output_path = os.path.join('data/resumes', filename)
        if not os.path.exists(output_path):
            # Process the file
            text, error = process_file(file)
            if error:
                return render_template(PAGE_INDEX_HTML, error=error)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(text)
        else:
            # Read the existing file
            print(f'File already exists: {output_path}')
            with open(output_path, "r", encoding="utf-8") as f:
                text = f.read()

        # ******************************
        # Perform job search
        # ******************************

        try:
            ################################################################
            # START - Uncomment below line to use a live job search service
            # jobs_data = SearchJobs(
            #     keywords, location, resume=output_path).search()
            # END - Uncomment above line to use the live job search service
            ################################################################
            ################################################################
            # START - Comment below lines to use the live job search results
            # Simulate job search results
            output_path = os.path.join('data/', 'sample_result.json')
            with open(output_path, "r", encoding="utf-8") as f:
                jobs_data = f.read()
            # END - Comment above lines to use the live job search results
            ################################################################

            if jobs_data is None:
                error = "Job search failed"
                return render_template(PAGE_INDEX_HTML, error=error)

            print(f'deserializing jobs_data: {jobs_data}')
            # jobs_data = json.loads(jobs_data)

            # Redirect to the result page with the extracted text and job search results
            # /result?text={text}&jobs={jobs_data}
            return redirect(url_for(
                "result",
                text=text,
                jobs=jobs_data,
                keywords=keywords,
                location=location
            ))

        except Exception as e:
            error = f"Error: {e}"
            return render_template(PAGE_INDEX_HTML, error=error)

    return render_template(PAGE_INDEX_HTML)


@app.route("/result", methods=["GET"])
def result():
    """
    Result page route.
    Returns:
        Rendered HTML template with the search results.
    """

    try:
        keywords = request.args.get("keywords", "")
        location = request.args.get("location", "")

        text = request.args.get("text", "")
        jobs = request.args.get("jobs", "")
        jobs = json.loads(jobs)
        if 'jobs' not in jobs:
            jobs = {"jobs": []}
        else:
            jobs = jobs['jobs']

    except Exception as e:
        print(f'Error decoding results: {e}')
        jobs = []

    return render_template(
        PAGE_RESULT_HTML,
        keywords=keywords,
        location=location,
        text=text,
        jobs=jobs
    )


if __name__ == "__main__":
    app.run(debug=True)
