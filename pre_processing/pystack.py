import argparse
import os.path
from process_comments import comments_processing
from process_badges import badges_processing
from process_votes import bounty_processing
from process_postlinks import postlinks_processing
from process_posts import posts_processing
from process_formulas import formula_processing

def preprocessing_main(cate_name, database_name):
	posts_processing(os.path.join(cate_name,"Posts.xml"), database_name)
	postlinks_processing(os.path.join(cate_name,"PostLinks.xml"), database_name)
	bounty_processing(os.path.join(cate_name,"Votes.xml"), database_name)
	badges_processing(os.path.join(cate_name,"Badges.xml"), database_name)
	comments_processing(os.path.join(cate_name,"Comments.xml"), database_name)
	formula_processing(cate_name, database_name)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-i","--input",default= "../dataset/mathematics", help = "input category name")
	parser.add_argument("-d", "--database", default='../database/dataset.db', help="output database")
	args = parser.parse_args()
	preprocessing_main(args.input, args.database)
