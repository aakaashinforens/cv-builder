import sys
from parse_cv import extract_text_from_file
from prompt_builder import build_prompt
from generate_cv import call_perplexity
from save import save_as_docx

def main():
    workflow = input("Choose workflow (new / existing): ").lower()
    user_data = {}
    prompt = None  # ensure prompt is defined
    
    if workflow == "new":
        has_work_exp = input("Do you have relevant work experience? (yes/no): ").strip().lower()
        if has_work_exp not in ("yes", "no"):
            print("Please answer yes or no")
            sys.exit(1)

        user_data = {
            "full_name": input("Full name: "),
            "target_country": input("Target country: "),
            "cv_length": input("CV length (1 or 2): (optional) "),
            "style": input("CV style (Formal / Modern / Creative / ATS-friendly / etc.): (optional) "),
            "email": input("Email: "),
            "phone": input("Phone number: "),
            "linkedin": input("LinkedIn URL (optional): "),
            "location": input("Location: (optional) "),
            "work_experience": input("Work Experience (paste or type, optional): "),
            "education": input("Education details (paste or type, optional): "),
            "skills": input("Skills: "),
            "certificates": input("Certificates and awards (optional): "),
            "projects": input("Projects (optional): ")
        }

        prompt = build_prompt(user_data)

    elif workflow == "existing":
        file_path = input("Path to CV file (PDF or DOCX): ").strip()
        raw_text = extract_text_from_file(file_path)

        choice = input("Reformat for a (country/company)? ").lower()
        if choice == "country":
            target = input("Enter target country: ")
            user_data["target_country"] = target
        else:  # company flow
            jd = input("Paste JD here: ")
            user_data["job_description"] = jd

        user_data["cv_length"] = input("CV length (1 or 2 pages): (optional) ")
        user_data["style"] = input("CV style (Formal / Modern / Creative / ATS-friendly / etc.): (optional) ")

        prompt = build_prompt(user_data, raw_text=raw_text)

    else:
        print("Invalid workflow")
        sys.exit(1)

    try:
        # Generate CV
        generated_cv = call_perplexity(prompt)
        print("\nGenerated CV:\n")
        print(generated_cv)

        download_choice = input("\nDo you want to download the CV as DOCX? (yes/no): ").strip().lower()
        if download_choice == "yes":
            save_as_docx(generated_cv)

        # --- Optional cover letter for company workflow ---
        if workflow == "existing" and choice == "company":
            cover_choice = input("\nDo you want to generate a cover letter for this JD? (yes/no): ").strip().lower()
            if cover_choice == "yes":
                cover_prompt = f"Using the CV below and the job description, create a professional cover letter:\n\nCV:\n{generated_cv}\n\nJD:\n{user_data['job_description']}"
                generated_cover = call_perplexity(cover_prompt)
                print("\nGenerated Cover Letter:\n")
                print(generated_cover)

                save_cover = input("\nDo you want to download the cover letter as DOCX? (yes/no): ").strip().lower()
                if save_cover == "yes":
                    save_as_docx(generated_cover, filename="cover_letter.docx")

    except Exception as e:
        print(f"Error generating CV/cover letter: {e}")


if __name__ == "__main__":
    main()
