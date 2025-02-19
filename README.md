# DataRefine-AI Case Study

## Overview

**DataRefine-AI** is an intelligent system developed to clean and prepare tabular datasets. Its primary goal is to transform messy, inconsistent, or incomplete datasets into clean, accurate, and analysis-ready data. DataRefine-AI automates the process of validating data, handling missing values through interpolation, removing duplicates, and normalizing data types. The system accepts input only in CSV or JSON formats (embedded within markdown code blocks) and enforces strict data validation rules before processing. Additionally, it provides clear, step-by-step explanations of every operation performed, making it accessible even to non-technical users.

## Features

- **Data Validation:**  
  DataRefine-AI thoroughly checks the input data for:
  - The correct file format (only CSV or JSON provided within markdown code blocks).
  - The presence of column headers.
  - Proper data types and structure.
  - Consistency in values, ensuring there are no severe issues like excessive missing values or conflicting duplicates.

- **Data Cleaning:**  
  The system cleans datasets using the following key processes:
  - **Handling Missing Values:**  
    For numeric fields, missing values are filled using linear interpolation. The formula used is:
    $$
    \text{Interpolated Value} = \text{Value}_{\text{left}} + \frac{(\text{Value}_{\text{right}} - \text{Value}_{\text{left}})}{(\text{Index}_{\text{right}} - \text{Index}_{\text{left}})} \times (\text{Missing Index} - \text{Index}_{\text{left}})
    $$
    If interpolation is not feasible (e.g., missing values at the beginning or end), mean imputation is used as a fallback. For categorical fields, missing entries are filled with the most frequent value or "Unknown."
  - **Removing Duplicates:**  
    The system identifies duplicate rows and removes them. If there are conflicting records for the same identifier, the user is prompted to review the conflicts and choose the preferred record.
  - **Normalizing Data Types:**  
    Text fields are standardized (e.g., consistent casing), date fields are formatted uniformly to `YYYY-MM-DD`, and numeric fields are ensured to be pure numbers without extraneous characters.

- **Step-by-Step Explanations:**  
  DataRefine-AI provides detailed explanations for each cleaning step, including the formulas used, making it easy to understand the process—even for someone with little technical background.

- **User Feedback and Iterative Improvement:**  
  After processing the data, the system presents a comprehensive summary report and asks for user feedback. This allows for iterative improvements based on user responses and ensures the final dataset meets their needs.

## System Prompt

The system prompt below governs the behavior of DataRefine-AI. It includes rules for language, data validation, cleaning steps, and response formatting:

```markdown
**[system]**
You are DataRefine-AI, an advanced assistant designed to clean and prepare tabular datasets. Your primary task is to process datasets by addressing missing values using linear interpolation (with fallback to mean imputation if necessary), removing duplicate records (with user review for conflicting entries), and normalizing data types. You accept data provided only in CSV or JSON format within markdown code blocks. Validate the input for proper formatting, headers, and data consistency. Provide clear, step-by-step explanations for each cleaning operation, and ask for user feedback after processing the data. If errors are encountered (e.g., unsupported format, missing headers, invalid data types), return structured error messages with instructions for correction.
```

## Metadata

- **Project Name:** DataRefine-AI  
- **Version:** 1.0.0  
- **Author:** Usman Ashfaq  
- **Keywords:** Data Cleaning, Tabular Data, Interpolation, Duplicate Removal, Data Normalization, Data Validation, Automation

## Variations and Test Flows

### Flow 1: Basic Greeting and Template Request
- **User Action:** Greets with "hi".
- **Assistant Response:** Greets back with a default message: "Hello! How can I assist you with cleaning your dataset today? If you need a template for structuring your data, just ask!"
- **User Action:** Accepts and requests the template.
- **Assistant Response:** Provides CSV and JSON template examples, then asks: "Please provide your dataset in CSV or JSON format, and I will clean it for you."
- **User Action:** Submits CSV data containing a dataset with missing values, duplicates, and inconsistencies.
- **Assistant Response:** Processes the data, fills missing values using linear interpolation, removes duplicates, normalizes data types, and returns a detailed transformation report.
- **Feedback:** The user rates the analysis positively.

### Flow 2: Time-Based Greeting and No Template Request
- **User Action:** Greets with "Good afternoon, I'm ready to work on cleaning my data."
- **Assistant Response:** Provides a time-appropriate greeting and asks if a template is needed.
- **User Action:** Declines the template and provides CSV data.
- **Assistant Response:** Processes the data as per cleaning workflow and returns a comprehensive summary report.
- **Feedback:** The user rates the analysis as 5, prompting a positive acknowledgment from the assistant.

### Flow 3: JSON Data with Errors and Corrections
- **User Action:** Provides JSON data with missing required fields.
- **Assistant Response:** Detects the missing field and returns an error message indicating the missing column header.
- **User Action:** Provides new JSON data with an invalid data type for one of the fields.
- **Assistant Response:** Returns an error message specifying the expected data type.
- **User Action:** Finally submits correct JSON data with all required fields.
- **Assistant Response:** Processes the data and returns a detailed cleaning report.
- **Feedback:** The user rates the analysis as 3, prompting the assistant to ask for improvement suggestions.

### Flow 4: JSON Data with Data Type Errors
- **User Action:** Provides JSON data with incorrect data types for some required fields.
- **Assistant Response:** Greets the user by name, points out the data type errors, and returns an error message.
- **User Action:** Provides corrected JSON data.
- **Assistant Response:** Processes the data and returns a detailed cleaning report.
- **Feedback:** The user rates the analysis as 3, and the assistant asks how the process can be improved.

## Conclusion

DataRefine-AI is a robust, flexible, and user-friendly tool that automates the cleaning of tabular datasets. It enforces strict validation rules and provides detailed, step-by-step explanations, making complex data cleaning operations transparent and understandable—even for non-technical users. The various test flows demonstrate how DataRefine-AI handles different scenarios, error conditions, and user feedback, ensuring continuous improvement in performance. This project exemplifies the power of automation in simplifying data preparation, ultimately aiding in accurate analysis and decision-making.

---
