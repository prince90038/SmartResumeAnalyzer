import json
from pipeline.resume_pipeline import process_resume, run_matching, run_scoring, run_analysis
from pipeline.jd_pipeline import process_jd

if __name__ == "__main__":
    # resume = process_resume("data/input/resume.pdf")
    #
    # with open("data/output/resume.json", "w") as f:
    #     json.dump(resume, f, indent=2)
    #
    # jd_text = open("data/input/jd.txt").read()
    # jd = process_jd(jd_text)
    #
    # with open("data/output/jd.json", "w") as f:
    #     json.dump(jd, f, indent=2)
    #
    # print("Phase 1 Done")

    # Run only if Phase 1 not executed before, else read from output directory
    # resume = process_resume("data/input/resume.pdf")
    # jd = process_jd(open("data/input/jd.txt").read())

    # Read resume and jd JSON from output directory
    with open("data/output/resume.json", "r") as f:
        resume = json.load(f)
    with open("data/output/jd.json", "r") as f:
        jd = json.load(f)

    # result = run_matching(resume, jd)
    # print("Phase 2 Done")
    #
    # result["score"] = run_scoring(result)
    # print("Phase 3 Done")

    with open("data/output/match.json", "r") as f:
        result = json.load(f)

    result["analysis"] = run_analysis(resume, jd, result)
    print("Phase 4 Done")

    with open("data/output/match.json", "w") as f:
        json.dump(result, f, indent=2)
