
def route_query(query):
    query = query.lower()

    attendance_keywords = {
        "attendance", "attend", "absent", "absence",
        "present", "percentage", "shortage"
    }

    library_keywords = {
        "library", "book", "books", "borrow",
        "return", "librarian", "reading"
    }

    selected_files = []

    if any(word in query for word in attendance_keywords):
        selected_files.append("attendance.txt")

    if any(word in query for word in library_keywords):
        selected_files.append("library.txt")

    if not selected_files:
        return []

    return selected_files

if __name__ == "__main__":
    while True:
        query = input("\nAsk a question (type 'exit' to quit): ")

        if query.lower() == "exit":
            break

        files = route_query(query)

        if files:
            print("Selected documents:", ", ".join(files))
        else:
            print("No matching document found.")