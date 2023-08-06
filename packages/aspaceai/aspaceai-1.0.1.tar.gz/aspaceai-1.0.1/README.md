# ASpace AI API: Python SDK & Sample


This repo contains the Python SDK for the ASpace AI cognitive services, an offering within [ASpace AI Cognitive Services](https://www.ey.com/en_in/consulting/accelerating-digital-transformation-with-ai)

* [Learn about EY ASpace AI Platform](https://www.ey.com/en_in/consulting/accelerating-digital-transformation-with-ai)


## Getting started

Install the module using [pip](https://pypi.python.org/pypi/pip/):

```bash
pip install aspaceai
```

Use it:

```python
import aspaceai

ASPACE_URL = 'https://demo.aspace.ai/aspace/v1.0/'  # Replace with your aspace endpoint URL
ASPACE_API_KEY = 'ASpace subscription key'  # Replace with a valid Subscription Key here.

text = "This is a great start to AI !!!"
result = aspaceai.sense.sentiment_analysis(text)
print (result)
```

### Installing from the source code

```bash
python setup.py install
```
![ASpace AI Themes](https://assets.ey.com/content/dam/ey-sites/ey-com/en_in/topics/consulting/2020/07/aspace/vison-sense.png.rendition.3840.2560.png)
## Contributing

We welcome contributions. Feel free to file issues and pull requests on the repo and we'll address them as we can. Learn more about how you can help on our [Contribution Rules & Guidelines](/CONTRIBUTING.md).

You can reach out to us anytime with questions and suggestions using our communities below:
 - **Support questions:** [StackOverflow](https://stackoverflow.com/questions/tagged/aspaceai)
 
## Updates
* [ASpace.ai Platform Release Notes](https://www.ey.com/en_in/consulting/accelerating-digital-transformation-with-ai)

## License
All ASpace Cognitive Services SDKs and samples are licensed with the MIT License. For more details, see
[LICENSE](/LICENSE.txt).



## Developer Code of Conduct
Developers using Cognitive Services, including this sample, are expected to follow the “Developer Code of Conduct for ASpace AI”, found at [https://www.ey.com/en_in/consulting/accelerating-digital-transformation-with-ai](https://www.ey.com/en_in/consulting/accelerating-digital-transformation-with-ai).