const API_KEY = 'AIzaSyBUu99wdleXyKZI-3nJj4gilJxTfvJ6zQU';
const API_URL = 'http://localhost:5005';

console.log('🎯 Dashboard script started');

// Get video ID and title from URL params
const params = new URLSearchParams(window.location.search);
const videoId = params.get('videoId');
const videoTitle = decodeURIComponent(params.get('videoTitle') || 'YouTube Video');
const returnTabId = params.get('returnTabId');
const returnUrl = decodeURIComponent(params.get('returnUrl') || '');
let closeInProgress = false;

console.log('📺 Video ID from URL:', videoId);
console.log('📺 Video Title from URL:', videoTitle);

function closeDashboard() {
    if (closeInProgress) {
        return;
    }

    closeInProgress = true;
    console.log('🔒 Close dashboard requested');

    const goBackToYouTube = () => {
        if (returnUrl && /^https:\/\/(www\.)?youtube\.com\//.test(returnUrl)) {
            console.log('↩️ Navigating back to YouTube URL');
            window.location.replace(returnUrl);
            return;
        }

        if (document.referrer && /^https:\/\/(www\.)?youtube\.com\//.test(document.referrer)) {
            console.log('↩️ Navigating back via history');
            window.history.back();
            return;
        }

        window.close();
    };

    const fallbackTimer = setTimeout(() => {
        console.warn('⚠️ Close request timed out, using fallback navigation');
        goBackToYouTube();
    }, 800);

    if (chrome?.runtime?.sendMessage) {
        chrome.runtime.sendMessage({
            action: 'closeDashboard',
            returnTabId,
            returnUrl
        }, (response) => {
            if (chrome.runtime.lastError) {
                console.warn('⚠️ Close request failed:', chrome.runtime.lastError.message);
                clearTimeout(fallbackTimer);
                goBackToYouTube();
                return;
            }

            if (!response || !response.success) {
                console.warn('⚠️ Background did not close dashboard:', response?.message || 'unknown error');
                clearTimeout(fallbackTimer);
                goBackToYouTube();
                return;
            }

            clearTimeout(fallbackTimer);
        });
    } else {
        clearTimeout(fallbackTimer);
        goBackToYouTube();
    }
}

function initializeDashboard(dashboardData) {
    console.log('🎨 Initializing dashboard');
    
    if (!dashboardData) {
        console.error('❌ No dashboard data');
        document.body.innerHTML = '<p style="color: #f44336; padding: 20px; font-size: 16px;">❌ Error: No data</p>';
        return;
    }
    
    try {
        document.getElementById('videoTitle').textContent = dashboardData.videoTitle || 'Video Analysis';
        document.getElementById('totalComments').textContent = dashboardData.totalComments;
        document.getElementById('positiveCount').textContent = dashboardData.sentimentCounts['1'] || 0;
        document.getElementById('neutralCount').textContent = dashboardData.sentimentCounts['0'] || 0;
        document.getElementById('negativeCount').textContent = dashboardData.sentimentCounts['-1'] || 0;
        document.getElementById('uniqueCommenters').textContent = dashboardData.uniqueCommenters;
        document.getElementById('avgCommentLength').textContent = dashboardData.avgCommentLength + ' words';
        document.getElementById('avgSentimentScore').textContent = dashboardData.avgSentimentScore + '/10';

        // Create pie chart
        const ctx = document.getElementById('sentimentChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Positive', 'Neutral', 'Negative'],
                datasets: [{
                    data: [
                        dashboardData.sentimentCounts['1'] || 0,
                        dashboardData.sentimentCounts['0'] || 0,
                        dashboardData.sentimentCounts['-1'] || 0
                    ],
                    backgroundColor: ['#4caf50', '#ff9800', '#f44336'],
                    borderColor: ['#45a049', '#fb8c00', '#da190b'],
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });

        // Render comments
        const commentsList = document.getElementById('commentsList');
        commentsList.innerHTML = '';

        if (dashboardData.predictions && dashboardData.predictions.length > 0) {
            dashboardData.predictions.forEach((item, index) => {
                const sentiment = item.sentiment;
                const sentimentLabel = sentiment === '1' ? 'positive' : sentiment === '0' ? 'neutral' : 'negative';
                const sentimentText = sentiment === '1' ? 'Positive' : sentiment === '0' ? 'Neutral' : 'Negative';

                const commentCard = document.createElement('div');
                commentCard.className = `comment-card ${sentimentLabel}`;
                commentCard.innerHTML = `
                    <div class="comment-header">
                        <span class="comment-number">Comment #${index + 1}</span>
                        <span class="sentiment-badge ${sentimentLabel}">${sentimentText}</span>
                    </div>
                    <div class="comment-text">${item.comment}</div>
                `;
                commentsList.appendChild(commentCard);
            });
        } else {
            commentsList.innerHTML = '<p style="color: #999;">No comments to display</p>';
        }
        
        console.log('✅ Dashboard loaded successfully');
    } catch (error) {
        console.error('❌ Error:', error);
        document.body.innerHTML = '<p style="color: #f44336; padding: 20px; font-size: 16px;">❌ ' + error.message + '</p>';
    }
}

// Fetch comments and sentiment analysis
async function fetchDashboardData() {
    console.log('📡 Fetching dashboard data for video:', videoId);
    
    try {
        // Check API health
        console.log('🔍 Checking API health...');
        try {
            const healthResponse = await fetch(`${API_URL}/health`);
            if (!healthResponse.ok) {
                throw new Error(`Health check failed: ${healthResponse.status}`);
            }
            const healthData = await healthResponse.json();
            console.log('✅ API Health:', healthData);
        } catch (err) {
            console.error('🚨 API Health check failed:', err);
            throw new Error(`Cannot connect to Flask API at ${API_URL}. Make sure it's running.`);
        }

        // Update UI to show we're fetching comments
        document.getElementById('videoTitle').textContent = videoTitle || 'Loading...';

        // Fetch comments
        console.log('💬 Fetching comments for video:', videoId);
        const comments = [];
        let pageToken = "";
        
        try {
            while (true) {
                console.log('📥 Fetching with pageToken:', pageToken || 'none');
                const response = await fetch(`https://www.googleapis.com/youtube/v3/commentThreads?part=snippet,replies&videoId=${videoId}&maxResults=100&pageToken=${pageToken}&textFormat=plainText&key=${API_KEY}`);
                
                if (!response.ok) {
                    const errorText = await response.text();
                    console.error('YT Response:', errorText);
                    throw new Error(`YouTube API error: ${response.status} ${errorText.substring(0, 100)}`);
                }
                
                const data = await response.json();
                console.log('📊 Got items:', data.items ? data.items.length : 0);
                
                if (data.error) {
                    throw new Error(`YouTube API Error: ${data.error.message}`);
                }
                
                if (data.items) {
                    data.items.forEach(item => {
                        const commentText = item.snippet.topLevelComment.snippet.textOriginal;
                        const timestamp = item.snippet.topLevelComment.snippet.publishedAt;
                        const authorId = item.snippet.topLevelComment.snippet.authorChannelId?.value || 'Unknown';
                        comments.push({ text: commentText, timestamp: timestamp, authorId: authorId });
                        
                        if (item.replies && item.replies.comments) {
                            item.replies.comments.forEach(reply => {
                                const replyText = reply.snippet.textOriginal;
                                const replyTimestamp = reply.snippet.publishedAt;
                                const replyAuthorId = reply.snippet.authorChannelId?.value || 'Unknown';
                                comments.push({ text: replyText, timestamp: replyTimestamp, authorId: replyAuthorId });
                            });
                        }
                    });
                }
                
                pageToken = data.nextPageToken;
                if (!pageToken) break;
            }
        } catch (err) {
            console.error('🚨 Error fetching comments:', err);
            throw new Error(`Failed to fetch comments: ${err.message}`);
        }
        
        console.log('✅ Fetched ' + comments.length + ' comments');

        if (comments.length === 0) {
            const msg = 'This video has no comments to analyze.';
            console.log('⚠️ ' + msg);
            document.getElementById('commentsList').innerHTML = '<p style="color: #999;">' + msg + '</p>';
            return;
        }

        // Get sentiment predictions
        console.log('🤖 Getting sentiment predictions from Flask...');
        let predictResponse;
        try {
            predictResponse = await fetch(`${API_URL}/predict_with_timestamps`, {
                method: "POST",
                headers: { 
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify({ comments })
            });
            
            if (!predictResponse.ok) {
                const errorText = await predictResponse.text();
                console.error('🚨 Flask Response:', errorText);
                throw new Error(`Flask API error: ${predictResponse.status} ${errorText.substring(0, 100)}`);
            }
            
            const predictions = await predictResponse.json();
            console.log('✅ Got ' + predictions.length + ' sentiment predictions');

            // Calculate metrics
            const sentimentCounts = { "1": 0, "0": 0, "-1": 0 };
            const totalSentimentScore = predictions.reduce((sum, item) => sum + parseInt(item.sentiment), 0);
            
            predictions.forEach((item) => {
                sentimentCounts[item.sentiment]++;
            });

            const totalComments = comments.length;
            const uniqueCommenters = new Set(comments.map(comment => comment.authorId)).size;
            const totalWords = comments.reduce((sum, comment) => sum + comment.text.split(/\s+/).filter(word => word.length > 0).length, 0);
            const avgWordLength = (totalWords / totalComments).toFixed(2);
            const avgSentimentScore = (totalSentimentScore / totalComments).toFixed(2);
            const normalizedSentimentScore = (((parseFloat(avgSentimentScore) + 1) / 2) * 10).toFixed(2);

            // Create dashboard object
            const dashboardData = {
                videoTitle: videoTitle,
                totalComments: totalComments,
                uniqueCommenters: uniqueCommenters,
                avgCommentLength: avgWordLength,
                avgSentimentScore: normalizedSentimentScore,
                sentimentCounts: sentimentCounts,
                predictions: predictions
            };

            console.log('📊 Dashboard data prepared:', dashboardData);
            initializeDashboard(dashboardData);
        } catch (predictErr) {
            console.error('🚨 Error with sentiment prediction:', predictErr);
            throw new Error(`Failed to get sentiment predictions: ${predictErr.message}`);
        }
    } catch (error) {
        console.error('❌ Error fetching data:', error);
        document.body.innerHTML = '<p style="color: #f44336; padding: 20px; font-size: 16px;">❌ Error: ' + error.message + '</p>';
    }
}

// Start loading when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    const closeButton = document.getElementById('closeDashboardBtn');
    if (closeButton) {
        closeButton.addEventListener('click', closeDashboard);
    }

    if (videoId) {
        console.log('🚀 Starting data fetch...');
        fetchDashboardData();
    } else {
        document.body.innerHTML = '<p style="color: #ff9800; padding: 20px;">⚠️ Video ID not found in URL</p>';
    }
});
