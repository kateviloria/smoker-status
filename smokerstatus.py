# parses through medical notes and classifies patient status (Smoker, Former Smoker, Nonsmoker, Unknown)


# imports
import argparse



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Classify patient smoker status.")
    parser.add_argument("csvfile", type=str, help="Name of .csv file with data.")