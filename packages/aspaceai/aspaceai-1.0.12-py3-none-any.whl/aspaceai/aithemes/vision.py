#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: sense.py
Description: ai solutions for each vision.
"""
#         Theme vision

import aspaceai
import aspaceai.utility.aspaceconnector as connector
import json
class vision:
    def ocr(image,image_format,language='eng'):
        """Perform OCR on a given image.
        Args:
            image: Image information on which to perform OCR.
            image_format: url, file ,base64string
            language: default = eng
            Supported Languages : ["afr","amh","ara","asm","aze","aze-cyrl","bel","ben","bod","bos","bul","cat","ceb","ces","chi-sim","chi-tra","chr","cym","dan",
                "dan-frak","deu","deu-frak","dev","dzo","ell","eng","enm","epo","est","eus","fas","fin","fra","frk","frm","gle","gle-uncial","glg","grc",
                 "guj","hat","heb","hin","hrv","hun","iku","ind","isl","ita","ita-old","jav","jpn","kan","kat","kat-old","kaz","khm","kir","kor","kur",
                 "lao","lat","lav","lit","mal","mar","mkd","mlt","msa","mya","nep","nld","nor","ori","pan","pol","por","pus","ron","rus","san","sin",
                 "slk","slk-frak","slv","spa","spa-old","sqi"]

        Returns:
            An OCR JSON result
        """
        try:
            api_url = aspaceai.ASPACE_URL+"?apikey="+aspaceai.ASPACE_API_KEY+"&language="+language+"&image_format="+image_format
            payload = {}
            payload['image'] = image
            json_payload =json.dumps(payload)

            response_from_aspace = connector.createJSONPostRequest(api_url,json_payload)

            result_message = {}
            result_message['status'] = 'success'
            result_message['message'] = response_from_aspace.text
        except  Exception as e:
            result_message = {}
            result_message['status'] = 'failed'
            result_message['message'] = str(e)


        return json.dumps(result_message)