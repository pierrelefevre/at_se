![åt.se logo](https://github.com/pierrelefevre/at_se/blob/main/frontend/public/android-chrome-192x192.png?raw=true)

# åt.se
[åt.se](https://åt.se) is a AI generated summary of the current news feed in Sweden.

## Why?
As the Swedish news aggregator [Omni](https://omni.se) started adding more ads, I thought it might be a cool idea to try to make AI summarize news and create a similar digest.
It turns out this is quite difficult, and the results aren't great. I do not recommend using åt.se as a primary news source.

## The code
The code behind åt consists of a buffed up scraper using the OpenAI API, as well as a Astro frontend.
News articles are scraped, summarized, grouped and then stored in a MongoDB database. This is then pulled from the database and built into HTML on the server side in the frontend.

## License
The code of åt.se is licensed under GPL-3, however åt.se owns none of the content as it is scraped from newspapers.

## Contributing
Check out the current [Issues](https://github.com/pierrelefevre/at_se/issues), or start a new one. You can also create a Pull Request.

## Screenshot
![screenshot of the åt.se homepage](https://github.com/user-attachments/assets/fef4ae51-ec88-47f0-a181-4ac5a668f693)

