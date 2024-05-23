# chatbot.py
import streamlit as st
import json
import os
from openai import OpenAI


# Initialize the OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("API key not found. Please set the OPENAI_API_KEY environment variable.")
else:
    client = OpenAI(api_key=api_key)

    # Initialize session state for messages if not already done
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.api_messages = [
            {"role": "system", "content": """# ROLE: You are a specialized ChatBot that is integrated into a Streamlit Dashboard built by a team of students in B BUS 441 A at University of Washington Bothell 

# BACKGROUND INFO: The dashboard is built off of an 80,000 row csv file of raw Customer Service Data from 2023 Amazon. The team of students are instructed to develop suggestions and recommendations for improving various customer service metrics.

# YOUR PERSONA: Always project confidence and enthusiasm when presenting your analysis. Dive deep into the specifics of the data rather than staying at a high level. Your ability to discuss detailed data points and generate insightful suggestions will make a strong impression, showcasing your integration into a well-trained dashboard. Feel free to direct users to various parts of the dashboard or help them with how to use it if they have any questions or want to see specific visuals.
### KNOWLEGE BASE ###

Due to the sheer size of the raw data, you are given a summary snapshot of important measurments. Use this to formulate your theories, responses, and expertise. 

Filter: ALL
CSATScore,Percentage: 5,69  4,13  1,13  3,3  2,2
AgentTenure,CSATScore: OJT,4.15  0-30,4.26  31-60,4.30  61-90,4.35  >90,4.28
ProductCategory,CSATScore: Affiliates,4.2  LifeStyle,4.11  Electronics,4.04  Books & General merchandise,4.03  Home,3.95  Home Appliances,3.71  Furniture,3.66  Mobile,3.65  GiftCard,3.23

Filter: PRODUCT CATEGORY
LifeStyle,CSATScore: 4.11
Electronics,CSATScore: 4.04
Mobile,CSATScore: 3.65
Home Appliances,CSATScore: 3.71
Furniture,CSATScore: 3.66
Home,CSATScore: 3.95
Books & General merchandise,CSATScore: 4.03
GiftCard,CSATScore: 3.23
Affiliates,CSATScore: 4.2

Filter: AGENT TENURE
>90,CSATScore: 4.28
OJT,CSATScore: 4.15
0-30,CSATScore: 4.26
31-60,CSATScore: 4.3
61-90,CSATScore: 4.35



Response Times
Affiliates: 0-30,134.69 31-60,544.56 61-90,463.00 >90,220.98 On Job Training,172.06
Books & General merchandise: 0-30,294.84 31-60,216.41 61-90,251.18 >90,302.78 On Job Training,441.48
Electronics: 0-30,167.06 31-60,123.45 61-90,229.76 >90,254.56 On Job Training,314.36
Furniture: 0-30,281.82 31-60,192.32 61-90,304.70 >90,384.58 On Job Training,371.81
GiftCard: 0-30,205.50 31-60,9.00 61-90,64.00 >90,679.10 On Job Training,1614.00
Home: 0-30,199.87 31-60,128.00 61-90,241.37 >90,322.82 On Job Training,449.29
Home Appliances: 0-30,330.80 31-60,237.23 61-90,258.98 >90,321.24 On Job Training,376.85
LifeStyle: 0-30,259.01 31-60,245.08 61-90,261.44 >90,287.94 On Job Training,417.93
Mobile: 0-30,143.96 31-60,196.25 61-90,245.22 >90,245.34 On Job Training,284.76

Ticket Volume
Affiliates: App Related,1 Cancellation,2 Feedback,6 Order Related,42 Refund Related,9 Returns,106
Books & General merchandise: App Related,3 Cancellation,181 Feedback,147 Order Related,1374 Refund Related,189 Returns,1405 Offers & Cashback,6 Others,7 Payments related,6 Product Queries,2
Electronics: Cancellation,177 Feedback,94 Order Related,1408 Refund Related,219 Returns,2731 Offers & Cashback,5 Others,5 Payments related,9 Product Queries,4
Furniture: Cancellation,37 Feedback,26 Order Related,218 Refund Related,23 Returns,144 Offers & Cashback,1 Others,1 Payments related,1 Product Queries,2
GiftCard: Feedback,2 Order Related,9 Refund Related,3 Returns,4 Offers & Cashback,6 Others,1 Payments related,1
Home: Cancellation,55 Feedback,62 Order Related,548 Refund Related,97 Returns,555 Offers & Cashback,4 Others,2 Payments related,2 Product Queries,1
Home Appliances: App Related,1 Cancellation,48 Feedback,43 Order Related,592 Refund Related,99 Returns,472 Offers & Cashback,9 Others,1 Payments related,6 Product Queries,6
LifeStyle: Cancellation,144 Feedback,120 Order Related,1141 Refund Related,358 Returns,2330 Offers & Cashback,4 Others,9 Payments related,11
Mobile: App Related,1 Cancellation,157 Feedback,36 Order Related,945 Refund Related,171 Returns,390 Offers & Cashback,24 Others,1 Payments related,13 Product Queries,2

Agent Tenure Average CSAT

0-30: Affiliates,3.88, Books & General merchandise,4.10, Electronics,4.21, Furniture,3.77, GiftCard,2.50, Home,4.02, Home Appliances,3.60, LifeStyle,4.04, Mobile,3.85
31-60: Affiliates,4.66, Books & General merchandise,4.08, Electronics,4.15, Furniture,3.92, GiftCard,3.00, Home,4.18, Home Appliances,3.87, LifeStyle,4.20, Mobile,3.65
61-90: Affiliates,3.62, Books & General merchandise,4.19, Electronics,4.07, Furniture,3.94, GiftCard,3.67, Home,3.92, Home Appliances,4.01, LifeStyle,4.22, Mobile,3.85
>90: Affiliates,4.19, Books & General merchandise,4.03, Electronics,4.08, Furniture,3.68, GiftCard,4.00, Home,3.89, Home Appliances,3.62, LifeStyle,4.17, Mobile,3.53
On Job Training: Affiliates,4.23, Books & General merchandise,3.89, Electronics,3.77, Furniture,3.27, GiftCard,2.00, Home,3.87, Home Appliances,3.69, LifeStyle,3.94, Mobile,3.62

Ticket Type Distribution
App Related: Account updation,150 General Enquiry,1683 Other Account Related Issues,22 Signup Issues,489 Unable to Login,7
App/website: App/website Related,10
Cancellation: Not Needed,1920 Return cancellation,292
Feedback: UnProfessional Behaviour,2294
Offers & Cashback: Affiliate Offers,183 Instant discount,78 Other Cashback,219
Onboarding related: Commission related,3 Seller onboarding,62
Order Related: Customer Requested Modifications,805 Delayed,7387 General Enquiry,252 Installation/demo,4116 Invoice request,1465 Order Verification,72 Order status enquiry,6922 Priority delivery,972 Seller Cancelled Order,1058 Unable to track,164
Others: Call back request,46 Call disconnected,40 Non Order related,1 Others,12
Payments related: Billing Related,57 Card/EMI,19 Online Payment Issues,1079 PayLater related,140 Payment pending,17 Payment related Queries,743 Wallet related,230 e-Gift Voucher,42
Product Queries: Policy Related,2 Product Specific Information,3588 Warranty related,78
Refund Related: COD Refund Details,85 Refund Enquiry,2665 Refund Related Issues,1799
Returns: Damaged,475 Exchange / Replacement,896 Fraudulent User,4108 General Enquiry,10 Missing,2556 Product related Issues,183 Return request,8523 Reverse Pickup Enquiry,22388 Self-Help,49 Service Center - Service Denial,58 Service Centres Related,1875 Wrong,2597


Top 20 (Unweighted)
AgentName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Pamela Robinson,4.96,23,1.17
Sean Gay,4.91,22,1.15
Virginia Lane,4.91,109,2.09
Taylor Nelson,4.89,45,1.4
Anthony Sims,4.87,38,1.32
Nancy Singh,4.86,37,1.31
Morgan Smith,4.86,44,1.39
John Hoffman,4.86,36,1.3
Kelly Thomas,4.86,63,1.59
Nicole Simpson DVM,4.85,20,1.13
Emily Hernandez,4.84,32,1.26
Linda Murray,4.84,80,1.77
Brian Williams,4.83,24,1.17
Kelsey Richardson,4.83,53,1.48
Gregory Robinson,4.82,40,1.34
Penny Lam,4.82,95,1.93
Brian Mcguire,4.82,83,1.8
Kathleen Mcdonald,4.82,22,1.15
Colleen Hall,4.81,48,1.43
Dr. Heather Lewis,4.81,148,2.48


Bottom 20 (Unweighted)
AgentName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Philip Harmon,1.81,21,1.0
Rebecca Miller,1.95,22,1.01
Curtis Mccarthy,2.1,30,1.06
Nicole Zavala,2.13,30,1.06
Virginia Mccormick,2.15,34,1.08
Charles Morales,2.24,33,1.08
Wesley Meyer,2.26,27,1.05
Pamela Perez,2.38,34,1.09
Tommy Davies,2.46,35,1.11
Veronica Anderson,2.54,35,1.11
Melissa Spence,2.55,20,1.03
Willie Flores,2.55,20,1.03
Alyssa Jones,2.56,25,1.06
Sarah Keller,2.63,38,1.14
Melinda Mills,2.64,22,1.04
Jason Wilson,2.65,20,1.03
Christine Castro,2.77,26,1.07
Amber Brown,2.82,22,1.05
Jonathan Moore,2.83,23,1.06
Curtis Hill,2.87,23,1.06


Top 20 (Weighted)
AgentName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Wendy Taylor,4.35,426,5.0
David Smith,4.63,264,3.61
Timothy Huff,4.58,259,3.53
Jamie Smith,3.96,249,3.09
Kayla Wilson,4.41,213,2.99
Julie Williams,4.61,196,2.91
Mrs. Jennifer Stone,4.39,199,2.84
Sharon Bullock,4.47,193,2.81
Matthew White PhD,4.38,190,2.75
Anthony Booth,4.65,176,2.72
Brianna Wolf,4.72,173,2.72
Jennifer Hernandez,4.69,172,2.69
Ryan Thompson,4.63,166,2.61
William Carey DVM,4.53,166,2.57
Tina Harrington,4.39,171,2.57
Brian Young,4.71,157,2.54
Rebecca Graham,4.23,173,2.53
Robert Lewis,4.8,151,2.51
Rebecca Walker,4.16,174,2.51
Cole Moore,4.63,156,2.51


Bottom 20 (Weighted)
AgentName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Philip Harmon,1.81,21,1.0
Rebecca Miller,1.95,22,1.01
Melissa Spence,2.55,20,1.03
Willie Flores,2.55,20,1.03
Jason Wilson,2.65,20,1.03
Melinda Mills,2.64,22,1.04
Wesley Meyer,2.26,27,1.05
Jennifer Cline,2.95,21,1.05
Amber Brown,2.82,22,1.05
Curtis Mccarthy,2.1,30,1.06
Joshua Oliver,2.91,22,1.06
Alyssa Jones,2.56,25,1.06
Nicole Zavala,2.13,30,1.06
Terri Lopez,3.37,19,1.06
Jonathan Moore,2.83,23,1.06
Cody Peters,3.1,21,1.06
Michael Jenkins,3.25,20,1.06
Tina Ramirez,3.47,19,1.06
Curtis Hill,2.87,23,1.06
Joshua Christensen,3.14,21,1.06



Top 20 (Unweighted)
SupervisorName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Landon Tanaka,4.43,1613,2.4
Elijah Yamaguchi,4.4,3798,4.7
Isabella Wong,4.38,1068,1.8
William Park,4.36,2676,3.49
Sophia Sato,4.36,1652,2.41
Ethan Nakamura,4.36,1562,2.32
Nathan Patel,4.36,3513,4.36
Lily Chen,4.34,1847,2.61
Logan Lee,4.34,2439,3.22
Brayden Wong,4.33,2515,3.3
Olivia Wang,4.33,2215,2.98
Amelia Tanaka,4.32,1354,2.08
Noah Patel,4.3,3383,4.18
Aiden Patel,4.3,2853,3.63
Madison Kim,4.29,2743,3.51
Abigail Suzuki,4.28,2198,2.94
Wyatt Kim,4.27,1711,2.44
Layla Taniguchi,4.27,911,1.61
Mia Patel,4.26,3249,4.01
Carter Park,4.25,4225,5.0


Bottom 20 (Unweighted)
SupervisorName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Oliver Nguyen,3.49,411,1.02
Sophia Chen,4.02,335,1.0
Zoe Yamamoto,4.04,3513,4.09
Harper Wong,4.07,1111,1.76
Dylan Kim,4.08,1189,1.84
Emma Park,4.08,3246,3.86
Charlotte Suzuki,4.09,1168,1.83
Mia Yamamoto,4.09,618,1.28
Austin Johnson,4.11,1705,2.36
Jacob Sato,4.16,1487,2.17
Mason Gupta,4.17,2096,2.78
Ava Wong,4.17,3342,4.03
Ethan Tan,4.17,1814,2.5
Olivia Suzuki,4.18,2156,2.84
Emily Yamashita,4.19,2547,3.24
Alexander Tanaka,4.19,1310,2.0
Jackson Park,4.2,2551,3.26
Lucas Singh,4.21,1262,1.95
Evelyn Kimura,4.24,2951,3.69
Scarlett Chen,4.25,2649,3.38


Top 20 (Weighted)
SupervisorName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Carter Park,4.25,4225,5.0
Elijah Yamaguchi,4.4,3798,4.7
Nathan Patel,4.36,3513,4.36
Noah Patel,4.3,3383,4.18
Zoe Yamamoto,4.04,3513,4.09
Ava Wong,4.17,3342,4.03
Mia Patel,4.26,3249,4.01
Emma Park,4.08,3246,3.86
Evelyn Kimura,4.24,2951,3.69
Aiden Patel,4.3,2853,3.63
Madison Kim,4.29,2743,3.51
William Park,4.36,2676,3.49
Scarlett Chen,4.25,2649,3.38
Brayden Wong,4.33,2515,3.3
Jackson Park,4.2,2551,3.26
Emily Yamashita,4.19,2547,3.24
Logan Lee,4.34,2439,3.22
Olivia Wang,4.33,2215,2.98
Abigail Suzuki,4.28,2198,2.94
Olivia Suzuki,4.18,2156,2.84


Bottom 20 (Weighted)
SupervisorName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Sophia Chen,4.02,335,1.0
Oliver Nguyen,3.49,411,1.02
Mia Yamamoto,4.09,618,1.28
Layla Taniguchi,4.27,911,1.61
Harper Wong,4.07,1111,1.76
Isabella Wong,4.38,1068,1.8
Charlotte Suzuki,4.09,1168,1.83
Dylan Kim,4.08,1189,1.84
Lucas Singh,4.21,1262,1.95
Alexander Tanaka,4.19,1310,2.0
Amelia Tanaka,4.32,1354,2.08
Jacob Sato,4.16,1487,2.17
Ethan Nakamura,4.36,1562,2.32
Austin Johnson,4.11,1705,2.36
Landon Tanaka,4.43,1613,2.4
Sophia Sato,4.36,1652,2.41
Wyatt Kim,4.27,1711,2.44
Ethan Tan,4.17,1814,2.5
Lily Chen,4.34,1847,2.61
Mason Gupta,4.17,2096,2.78


Top 5 (Unweighted)
ManagerName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Emily Chen,4.38,13913,2.93
John Smith,4.27,24962,5.0
Michael Lee,4.26,17413,3.53
Jennifer Nguyen,4.16,15740,3.13
William Kim,4.12,8483,1.75


Bottom 5 (Unweighted)
ManagerName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Olivia Tan,4.12,4475,1.0
William Kim,4.12,8483,1.75
Jennifer Nguyen,4.16,15740,3.13
Michael Lee,4.26,17413,3.53
John Smith,4.27,24962,5.0


Top 5 (Weighted)
ManagerName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
John Smith,4.27,24962,5.0
Michael Lee,4.26,17413,3.53
Jennifer Nguyen,4.16,15740,3.13
Emily Chen,4.38,13913,2.93
William Kim,4.12,8483,1.75


Bottom 5 (Weighted)
ManagerName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Olivia Tan,4.12,4475,1.0
William Kim,4.12,8483,1.75
Emily Chen,4.38,13913,2.93
Jennifer Nguyen,4.16,15740,3.13
Michael Lee,4.26,17413,3.53


Top 20 Pairs (Unweighted)
AgentName,SupervisorName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Pamela Robinson,Madison Kim,4.96,23,1.17
Sean Gay,Mia Patel,4.91,22,1.15
Virginia Lane,Sophia Sato,4.91,109,2.09
Taylor Nelson,Zoe Yamamoto,4.89,45,1.4
Anthony Sims,Zoe Yamamoto,4.87,38,1.32
Nancy Singh,Noah Patel,4.86,37,1.31
Morgan Smith,Isabella Wong,4.86,44,1.39
John Hoffman,Scarlett Chen,4.86,36,1.3
Kelly Thomas,Scarlett Chen,4.86,63,1.59
Nicole Simpson DVM,Mason Gupta,4.85,20,1.13
Emily Hernandez,Zoe Yamamoto,4.84,32,1.26
Linda Murray,Landon Tanaka,4.84,80,1.77
Brian Williams,Olivia Suzuki,4.83,24,1.17
Kelsey Richardson,Madison Kim,4.83,53,1.48
Gregory Robinson,Brayden Wong,4.82,40,1.34
Penny Lam,Elijah Yamaguchi,4.82,95,1.93
Brian Mcguire,Elijah Yamaguchi,4.82,83,1.8
Kathleen Mcdonald,Mia Patel,4.82,22,1.15
Colleen Hall,Landon Tanaka,4.81,48,1.43
Dr. Heather Lewis,Elijah Yamaguchi,4.81,148,2.48


Bottom 20 Pairs (Unweighted)
AgentName,SupervisorName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Philip Harmon,Emma Park,1.81,21,1.0
Rebecca Miller,Oliver Nguyen,1.95,22,1.01
Curtis Mccarthy,Zoe Yamamoto,2.1,30,1.06
Nicole Zavala,Oliver Nguyen,2.13,30,1.06
Virginia Mccormick,Zoe Yamamoto,2.15,34,1.08
Charles Morales,Zoe Yamamoto,2.24,33,1.08
Wesley Meyer,Zoe Yamamoto,2.26,27,1.05
Pamela Perez,Zoe Yamamoto,2.38,34,1.09
Tommy Davies,Ava Wong,2.46,35,1.11
Veronica Anderson,Zoe Yamamoto,2.54,35,1.11
Melissa Spence,Zoe Yamamoto,2.55,20,1.03
Willie Flores,Oliver Nguyen,2.55,20,1.03
Alyssa Jones,Zoe Yamamoto,2.56,25,1.06
Sarah Keller,Zoe Yamamoto,2.63,38,1.14
Melinda Mills,Emma Park,2.64,22,1.04
Jason Wilson,Zoe Yamamoto,2.65,20,1.03
Christine Castro,Zoe Yamamoto,2.77,26,1.07
Amber Brown,Carter Park,2.82,22,1.05
Jonathan Moore,Zoe Yamamoto,2.83,23,1.06
Curtis Hill,Emma Park,2.87,23,1.06


Top 20 Pairs (Weighted)
AgentName,SupervisorName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Wendy Taylor,Madison Kim,4.35,426,5.0
David Smith,Nathan Patel,4.63,264,3.61
Timothy Huff,Aiden Patel,4.58,259,3.53
Jamie Smith,Scarlett Chen,3.96,249,3.09
Kayla Wilson,Evelyn Kimura,4.41,213,2.99
Julie Williams,Zoe Yamamoto,4.61,196,2.91
Mrs. Jennifer Stone,Dylan Kim,4.39,199,2.84
Sharon Bullock,Scarlett Chen,4.47,193,2.81
Matthew White PhD,Scarlett Chen,4.38,190,2.75
Anthony Booth,William Park,4.65,176,2.72
Brianna Wolf,Mia Patel,4.72,173,2.72
Jennifer Hernandez,Lily Chen,4.69,172,2.69
Ryan Thompson,Olivia Wang,4.63,166,2.61
William Carey DVM,William Park,4.53,166,2.57
Tina Harrington,Carter Park,4.39,171,2.57
Brian Young,Elijah Yamaguchi,4.71,157,2.54
Rebecca Graham,Alexander Tanaka,4.23,173,2.53
Robert Lewis,Logan Lee,4.8,151,2.51
Rebecca Walker,Logan Lee,4.16,174,2.51
Cole Moore,Emma Park,4.63,156,2.51


Bottom 20 Pairs (Weighted)
AgentName,SupervisorName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Philip Harmon,Emma Park,1.81,21,1.0
Rebecca Miller,Oliver Nguyen,1.95,22,1.01
Melissa Spence,Zoe Yamamoto,2.55,20,1.03
Willie Flores,Oliver Nguyen,2.55,20,1.03
Jason Wilson,Zoe Yamamoto,2.65,20,1.03
Melinda Mills,Emma Park,2.64,22,1.04
Wesley Meyer,Zoe Yamamoto,2.26,27,1.05
Jennifer Cline,Logan Lee,2.95,21,1.05
Amber Brown,Carter Park,2.82,22,1.05
Curtis Mccarthy,Zoe Yamamoto,2.1,30,1.06
Joshua Oliver,William Park,2.91,22,1.06
Alyssa Jones,Zoe Yamamoto,2.56,25,1.06
Nicole Zavala,Oliver Nguyen,2.13,30,1.06
Terri Lopez,Dylan Kim,3.37,19,1.06
Jonathan Moore,Zoe Yamamoto,2.83,23,1.06
Cody Peters,Abigail Suzuki,3.1,21,1.06
Michael Jenkins,Emma Park,3.25,20,1.06
Tina Ramirez,Zoe Yamamoto,3.47,19,1.06
Curtis Hill,Emma Park,2.87,23,1.06
Joshua Christensen,Ava Wong,3.14,21,1.06


Top 20 Pairs (AgentName to ManagerName) (Unweighted)
AgentName,ManagerName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Pamela Robinson,Emily Chen,4.96,23,1.17
Sean Gay,Olivia Tan,4.91,22,1.15
Virginia Lane,John Smith,4.91,109,2.09
Taylor Nelson,Emily Chen,4.89,45,1.4
Anthony Sims,John Smith,4.87,38,1.32
Nancy Singh,Emily Chen,4.86,37,1.31
Morgan Smith,Emily Chen,4.86,44,1.39
John Hoffman,John Smith,4.86,36,1.3
Kelly Thomas,John Smith,4.86,63,1.59
Nicole Simpson DVM,Olivia Tan,4.85,20,1.13
Emily Hernandez,Emily Chen,4.84,32,1.26
Linda Murray,Emily Chen,4.84,80,1.77
Brian Williams,Jennifer Nguyen,4.83,24,1.17
Kelsey Richardson,Emily Chen,4.83,53,1.48
Gregory Robinson,John Smith,4.82,40,1.34
Penny Lam,Emily Chen,4.82,95,1.93
Brian Mcguire,Emily Chen,4.82,83,1.8
Kathleen Mcdonald,Olivia Tan,4.82,22,1.15
Colleen Hall,John Smith,4.81,48,1.43
Dr. Heather Lewis,Emily Chen,4.81,148,2.48


Bottom 20 Pairs (AgentName to ManagerName) (Unweighted)
AgentName,ManagerName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Philip Harmon,John Smith,1.81,21,1.0
Rebecca Miller,John Smith,1.95,22,1.01
Curtis Mccarthy,John Smith,2.1,30,1.06
Nicole Zavala,John Smith,2.13,30,1.06
Virginia Mccormick,John Smith,2.15,34,1.08
Charles Morales,John Smith,2.24,33,1.08
Wesley Meyer,John Smith,2.26,27,1.05
Pamela Perez,John Smith,2.38,34,1.09
Tommy Davies,Olivia Tan,2.46,35,1.11
Veronica Anderson,John Smith,2.54,35,1.11
Melissa Spence,John Smith,2.55,20,1.03
Willie Flores,John Smith,2.55,20,1.03
Alyssa Jones,John Smith,2.56,25,1.06
Sarah Keller,John Smith,2.63,38,1.14
Melinda Mills,John Smith,2.64,22,1.04
Jason Wilson,John Smith,2.65,20,1.03
Christine Castro,John Smith,2.77,26,1.07
Amber Brown,Jennifer Nguyen,2.82,22,1.05
Jonathan Moore,John Smith,2.83,23,1.06
Curtis Hill,John Smith,2.87,23,1.06


Top 20 Pairs (AgentName to ManagerName) (Weighted)
AgentName,ManagerName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Wendy Taylor,Michael Lee,4.35,426,5.0
David Smith,John Smith,4.63,264,3.61
Timothy Huff,John Smith,4.58,259,3.53
Jamie Smith,John Smith,3.96,249,3.09
Kayla Wilson,John Smith,4.41,213,2.99
Julie Williams,William Kim,4.61,196,2.91
Mrs. Jennifer Stone,Michael Lee,4.39,199,2.84
Sharon Bullock,John Smith,4.47,193,2.81
Matthew White PhD,John Smith,4.38,190,2.75
Anthony Booth,John Smith,4.65,176,2.72
Brianna Wolf,John Smith,4.72,173,2.72
Jennifer Hernandez,Michael Lee,4.69,172,2.69
Ryan Thompson,Emily Chen,4.63,166,2.61
William Carey DVM,John Smith,4.53,166,2.57
Tina Harrington,Michael Lee,4.39,171,2.57
Brian Young,Emily Chen,4.71,157,2.54
Rebecca Graham,Michael Lee,4.23,173,2.53
Robert Lewis,Emily Chen,4.8,151,2.51
Rebecca Walker,Emily Chen,4.16,174,2.51
Cole Moore,John Smith,4.63,156,2.51


Bottom 20 Pairs (AgentName to ManagerName) (Weighted)
AgentName,ManagerName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Philip Harmon,John Smith,1.81,21,1.0
Rebecca Miller,John Smith,1.95,22,1.01
Melissa Spence,John Smith,2.55,20,1.03
Willie Flores,John Smith,2.55,20,1.03
Jason Wilson,John Smith,2.65,20,1.03
Melinda Mills,John Smith,2.64,22,1.04
Wesley Meyer,John Smith,2.26,27,1.05
Jennifer Cline,Jennifer Nguyen,2.95,21,1.05
Amber Brown,Jennifer Nguyen,2.82,22,1.05
Curtis Mccarthy,John Smith,2.1,30,1.06
Joshua Oliver,Jennifer Nguyen,2.91,22,1.06
Alyssa Jones,John Smith,2.56,25,1.06
Nicole Zavala,John Smith,2.13,30,1.06
Terri Lopez,Jennifer Nguyen,3.37,19,1.06
Jonathan Moore,John Smith,2.83,23,1.06
Cody Peters,William Kim,3.1,21,1.06
Michael Jenkins,Jennifer Nguyen,3.25,20,1.06
Tina Ramirez,John Smith,3.47,19,1.06
Curtis Hill,John Smith,2.87,23,1.06
Joshua Christensen,William Kim,3.14,21,1.06


Top 5 Pairs (SupervisorName to ManagerName) (Unweighted)
SupervisorName,ManagerName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Nathan Patel,John Smith,4.58,830,2.33
Zoe Yamamoto,Emily Chen,4.53,480,1.75
Mason Gupta,Olivia Tan,4.51,188,1.27
Landon Tanaka,Emily Chen,4.49,1058,2.67
Elijah Yamaguchi,Emily Chen,4.49,1561,3.48


Bottom 5 Pairs (SupervisorName to ManagerName) (Unweighted)
SupervisorName,ManagerName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Oliver Nguyen,John Smith,3.49,411,1.48
Dylan Kim,Jennifer Nguyen,3.61,168,1.18
Lily Chen,William Kim,3.64,56,1.04
Olivia Wang,William Kim,3.68,63,1.05
Noah Patel,Jennifer Nguyen,3.69,80,1.07


Top 5 Pairs (SupervisorName to ManagerName) (Weighted)
SupervisorName,ManagerName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Scarlett Chen,John Smith,4.25,2649,5.0
Noah Patel,Michael Lee,4.32,2361,4.62
William Park,John Smith,4.41,2303,4.61
Carter Park,Michael Lee,4.27,2292,4.47
Emma Park,John Smith,4.07,2329,4.37


Bottom 5 Pairs (SupervisorName to ManagerName) (Weighted)
SupervisorName,ManagerName,AvgCSATScore,InteractionVolume,WeightedAvgCSATScore
Carter Park,William Kim,4.23,22,1.0
Austin Johnson,Jennifer Nguyen,3.72,25,1.0
Lily Chen,William Kim,3.64,56,1.04
Olivia Wang,William Kim,3.68,63,1.05
Dylan Kim,William Kim,3.77,62,1.05
"""}
        ]

def chatbot_ui():
    st.title("Chat with an AI Dashboard Assistant")

    # Custom CSS to improve chat message visibility and styling
    st.markdown("""
<style>
    /* Targets only the chat input field and not other input elements */
    .stTextInput .st-bk {
        background-color: #ffffff; /* Set desired background color for the input field */
    }

    .stTextInput .st-bk:focus {
        background-color: #ffffff; /* Keeps the background color the same when focused */
    }

    .chat-message {
        padding: 10px;
        margin: 5px;
        border-radius: 20px;
        border: 1px solid #ccc;
    }
    .chat-message.user {
        background-color: #e8f0fe; /* User message background */
        color: black; /* User message text color */
        text-align: right;
        float: right; /* Ensure right alignment */
        clear: both; /* Avoid floating issues */
    }
    .chat-message.assistant {
        background-color: #d1eaff; /* Assistant message background */
        color: black; /* Assistant message text color */
        text-align: left;
        float: left; /* Ensure left alignment */
        clear: both; /* Avoid floating issues */
    }
</style>
    """, unsafe_allow_html=True)

    # Display the messages
    for message in st.session_state.messages:
        with st.container():
            role_class = "user" if message["role"] == "user" else "assistant"
            st.markdown(f'<div class="chat-message {role_class}">{message["content"]}</div>', unsafe_allow_html=True)

    # Handle user input
    user_input = st.chat_input("Type your message...", key="user_input")
    if user_input is not None:
        process_user_input(user_input)

def process_user_input(user_input):
    # Append user message to session states
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.api_messages.append({"role": "user", "content": user_input})
    
    try:
        # Call the OpenAI API to get a response
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=st.session_state.api_messages
        )
        # Extract the assistant's message from the response
        assistant_message = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        st.session_state.api_messages.append({"role": "assistant", "content": assistant_message})
        
        # Immediate display update after API call
        st.rerun()
    except Exception as e:
        st.session_state.messages.append({"role": "assistant", "content": f"Failed to get response: {e}"})
        st.rerun() 
