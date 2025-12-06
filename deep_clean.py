import pandas as pd


def extract_details(df, col="details"):
	s = df[col].astype(str)
	df = df.copy()
	df["savings"] = s.str.extract(r"(\$?[0-9,\.]+)(?=\s+[Ss]avings)", expand=False)
	df["contract_total"] = s.str.extract(r"(\$?[0-9,\.]+)(?=\s+[Tt]otal)", expand=False)
	df["contract_description"] = s.str.extract(r"(?i)Total Contract\s+(.*)", expand=False)
	df["grant_description"] = s.str.extract(r"(?i)Total Grant\s+(.*)", expand=False)
	df["providing_agency"] = s.str.extract(r"(?i)Agency:\s*([^$]+)", expand=False)
	df["vendor"] = s.str.extract(r"^(.*?)\s*[Aa]gency:", expand=False)
	df["vendor"] = df["vendor"].str.lower()
	df["full_details"] = s.str.lower()
	# strip whitespace from some extracted fields
	for c in ["contract_description", "grant_description", "providing_agency", "vendor"]:
		if c in df.columns:
			df[c] = df[c].astype(str).str.strip().replace({'nan': None})
	return df


def main():

	df = pd.read_csv("data/doge_data.csv")
	df_clean = extract_details(df, col="details")
	# drop the original 'details' column per request
	df_clean = df_clean.drop(columns=["details"], errors="ignore")
	df_clean.to_csv("data/clean_cuts.csv", index=False)


if __name__ == "__main__":
	main()
