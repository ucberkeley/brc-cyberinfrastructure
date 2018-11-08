#!/bin/bash


clean () {
  echo "$3" > "$2"
  tail -n +2 "$1" >> "$2"
}

# Clean BRC Projects
PROJECTS_ORIGINAL_FILE="BRC-Projects - All-Projects.csv"
PROJECTS_CLEANED_FILE="projects-cleaned.csv"
PROJECTS_HEADER="Contact Name,Empty1,Project Name,Main Contacts Name,Main Contacts Email,Faculty Name,Faculty Email,Number,Empty2,Empty3,Empty4,Empty5,Empty6,Empty7,Empty8,Empty9"
clean "$PROJECTS_ORIGINAL_FILE" "$PROJECTS_CLEANED_FILE" "$PROJECTS_HEADER"

# Clearn BRC Project Requests
REQUESTS_ORIGINAL_FILE="Savio Project Requests - Project-Requests.csv"
REQUESTS_CLEANED_FILE="requests-cleaned.csv"
REQUESTS_HEADER=$(head -n1 "$REQUESTS_ORIGINAL_FILE")
clean "$REQUESTS_ORIGINAL_FILE" "$REQUESTS_CLEANED_FILE" "$REQUESTS_HEADER"
