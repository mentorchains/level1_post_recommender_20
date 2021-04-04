from flask import Flask,render_template,url_for,request
import model

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/predict',methods=['POST'])
def predict():
	if request.method == 'POST':
		post_title = request.form['post_title']
		post_body = request.form['post_body']
		post = post_title + ' ' + post_body
		my_prediction = model.predict(post)
	return render_template('result.html', prediction = my_prediction)

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=80, debug=True)