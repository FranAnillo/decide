from django.test import TestCase

# Create your tests here.
def test_facebook(self):
	self.driver.get(https://equipo1decide.herokuapp.com/visualizer/1/)
	self.driver.set_window_size(1298, 863)
	self.driver.find_elements(By.CSS_SELECTOR, "a:nth-child(2) > img").click()
	assert self.driver.find_elements(By.ID, "homelink").text == "Facebook"