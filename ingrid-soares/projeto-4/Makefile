# Makefile for UDA Pipeline Project

.PHONY: run clean seed process

# Default target: runs the full cycle
run: clean seed process

# Cleans up database files
clean:
	@echo "Cleaning up database..."
	rm -rf data/*.db

# Seeds the database with test documents
seed:
	@echo "Seeding database with test documents..."
	python3 seed_data.py

# Runs the main UDA pipeline
process:
	@echo "Running UDA Pipeline..."
	python3 run_pipeline.py
