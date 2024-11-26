from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def preprocess_and_find_similar_companies(processed_texts, gpt_answer, stopwords, financial, mktcap, ni_target, teq_target, ebitda_target):
    company_names = processed_texts['coname'].unique().tolist()
    for name in company_names:
        gpt_answer = gpt_answer.replace(name, '')
    words = gpt_answer.split()
    gpt_answer_cleaned = ' '.join([word for word in words if word not in stopwords])

    corpus = processed_texts['processed_text'].tolist() + [gpt_answer_cleaned]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    similarity_matrix = cosine_similarity(tfidf_matrix)
    similarities = similarity_matrix[-1, :-1]

    processed_texts['similarity'] = similarities
    top_5 = processed_texts.nlargest(5, 'similarity')
    filtered_top_5 = top_5[top_5['similarity'] > 0.15]

    if filtered_top_5.empty:
        return None, None, None, None, None, None, None, None, None, None

    similar_tickers = filtered_top_5['ticker'].tolist()
    selected_financials = financial[financial['ticker'].isin(similar_tickers)].copy()
    if selected_financials.empty:
        return None, None, None, None, None, None, None, None, None, None

    selected_financials['PER'] = selected_financials[mktcap] / selected_financials['ni']
    selected_financials['PBR'] = selected_financials[mktcap] / selected_financials['teq']
    selected_financials['EBITDA'] = selected_financials['oiadp'] + selected_financials['dp'] + selected_financials['amort']
    selected_financials['EV_adjustment'] = selected_financials['ibd'] - selected_financials['che']
    selected_financials['EV'] = selected_financials[mktcap] + selected_financials['EV_adjustment']
    selected_financials.loc[selected_financials['EV_adjustment'] < 0, 'EV'] = selected_financials[mktcap]
    selected_financials['EV_EBITDA'] = selected_financials['EV'] / selected_financials['EBITDA']

    for col in ['PER', 'PBR', 'EV_EBITDA']:
        selected_financials[col] = selected_financials[col].replace([np.inf, -np.inf], np.nan)

    filtered_top_5 = filtered_top_5.merge(
        selected_financials[['ticker', 'PER', 'PBR', 'EV_EBITDA']],
        how='left',
        on='ticker'
    )

    valid_per = selected_financials[selected_financials['ni'] > 0]['PER']
    valid_pbr = selected_financials[selected_financials['teq'] > 0]['PBR']
    valid_ev_ebitda = selected_financials[selected_financials['EBITDA'] > 0]['EV_EBITDA']

    excluded_per_count = len(selected_financials) - len(valid_per)
    excluded_ev_ebitda_count = len(selected_financials) - len(valid_ev_ebitda)

    average_per = valid_per.mean() if not valid_per.empty else None
    average_pbr = valid_pbr.mean() if not valid_pbr.empty else None
    average_ev_ebitda = valid_ev_ebitda.mean() if not valid_ev_ebitda.empty else None

    per_based_value = (average_per * ni_target) / 1e8 if average_per else None
    pbr_based_value = (average_pbr * teq_target) / 1e8 if average_pbr else None
    ev_ebitda_based_value = (average_ev_ebitda * ebitda_target) / 1e8 if average_ev_ebitda else None

    average_value = np.nanmean([v for v in [per_based_value, pbr_based_value, ev_ebitda_based_value] if v is not None])

    return (filtered_top_5, per_based_value, pbr_based_value, ev_ebitda_based_value, 
            average_value, excluded_per_count, excluded_ev_ebitda_count, 
            average_per, average_pbr, average_ev_ebitda)
