#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: sense.py
Description: ai solutions for each Sense.
"""
#         Theme Sense

import aspaceai
import aspaceai.utility.aspaceconnector as connector
import json
class sense:
    def sentiment_analysis(text_to_analyze):
        """Perform Sentiment analysis for a given text.
        Args:
            text: Text on which to perform sentiment analysis.

        Returns:
            An array of sentiment analysis and corresponding confidence factor.
        """
        print(aspaceai.ASPACE_URL)
        print(aspaceai.ASPACE_API_KEY)

        payload = {}
        payload['text'] = text_to_analyze
        json_payload =json.dumps(payload)
        result = connector.createJSONPostRequest(aspaceai.ASPACE_URL,json_payload)
        print(result)

        return "sentiment analysis"