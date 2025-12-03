'use client';

import { useState } from 'react';
import { Sparkles, Settings, Loader2, Download, TrendingUp, Edit3, CheckCircle, ChevronRight, ChevronDown } from 'lucide-react';
import { apiClient, GenerateResponse, GenerationSettings } from '@/lib/api';
import ReactMarkdown from 'react-markdown';

export default function Home() {
  const [topic, setTopic] = useState('');
  const [platform, setPlatform] = useState<'twitter' | 'linkedin'>('twitter');
  const [settings, setSettings] = useState<GenerationSettings>({
    model: 'meta-llama/llama-4-scout-17b-16e-instruct',
    maxIterations: 3,
    viralityThreshold: 85,
  });
  const [isGenerating, setIsGenerating] = useState(false);
  const [result, setResult] = useState<GenerateResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'content' | 'research' | 'feedback'>('content');

  const handleGenerate = async () => {
    if (!topic.trim()) {
      setError('Please enter a topic');
      return;
    }

    setIsGenerating(true);
    setError(null);
    setResult(null);

    try {
      const response = await apiClient.generateContent({
        topic,
        platform,
        settings,
      });
      setResult(response);
      setActiveTab('content');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsGenerating(false);
    }
  };

  const downloadContent = () => {
    if (!result) return;
    const blob = new Blob([result.final_content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `viral_${platform}_${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-background text-foreground font-sans selection:bg-primary/10">
      <div className="max-w-6xl mx-auto p-6 lg:p-12">
        {/* Header */}
        <div className="text-center mb-12 space-y-4">
          <div className="inline-flex items-center justify-center p-3 bg-white rounded-2xl shadow-sm border border-border mb-2">
            <Sparkles className="w-6 h-6 text-primary" />
          </div>
          <h1 className="text-4xl lg:text-5xl font-serif font-medium text-foreground tracking-tight">
            Viral Content Agent
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto font-light">
            Transform mundane topics into engaging social media narratives with our multi-agent AI team.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          {/* Sidebar Settings */}
          <div className="lg:col-span-4 space-y-6">
            <div className="bg-card rounded-xl border border-border p-6 shadow-sm">
              <div className="flex items-center gap-2 mb-6 text-primary">
                <Settings className="w-5 h-5" />
                <h2 className="font-serif text-lg font-medium">Configuration</h2>
              </div>

              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium mb-2 text-muted-foreground">Model</label>
                  <select
                    value={settings.model}
                    onChange={(e) => setSettings({ ...settings, model: e.target.value })}
                    className="w-full px-3 py-2.5 bg-secondary/50 border border-border rounded-lg text-sm focus:ring-1 focus:ring-primary focus:border-primary outline-none transition-all"
                  >
                    <option value="meta-llama/llama-4-scout-17b-16e-instruct">Llama 4 Scout</option>
                    <option value="meta-llama/llama-4-maverick-17b-128e-instruct">Llama 4 Maverick</option>
                    <option value="openai/gpt-oss-120b">GPT OSS 120B</option>
                    <option value="llama-3.3-70b-versatile">Llama 3.3 70B</option>
                  </select>
                </div>

                <div>
                  <div className="flex justify-between mb-2">
                    <label className="text-sm font-medium text-muted-foreground">Max Iterations</label>
                    <span className="text-sm text-primary font-mono">{settings.maxIterations}</span>
                  </div>
                  <input
                    type="range"
                    min="1"
                    max="5"
                    value={settings.maxIterations}
                    onChange={(e) => setSettings({ ...settings, maxIterations: parseInt(e.target.value) })}
                    className="w-full h-2 bg-secondary rounded-lg appearance-none cursor-pointer accent-primary"
                  />
                </div>

                <div>
                  <div className="flex justify-between mb-2">
                    <label className="text-sm font-medium text-muted-foreground">Virality Threshold</label>
                    <span className="text-sm text-primary font-mono">{settings.viralityThreshold}</span>
                  </div>
                  <input
                    type="range"
                    min="50"
                    max="100"
                    value={settings.viralityThreshold}
                    onChange={(e) => setSettings({ ...settings, viralityThreshold: parseInt(e.target.value) })}
                    className="w-full h-2 bg-secondary rounded-lg appearance-none cursor-pointer accent-primary"
                  />
                </div>
              </div>

              <div className="mt-8 pt-6 border-t border-border">
                <h3 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-4">Active Agents</h3>
                <div className="space-y-3">
                  <div className="flex items-center gap-3 text-sm p-2 rounded-lg bg-secondary/30">
                    <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center border border-border shadow-sm">
                      <TrendingUp className="w-4 h-4 text-primary" />
                    </div>
                    <div>
                      <div className="font-medium">Trend Scout</div>
                      <div className="text-xs text-muted-foreground">Researcher</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3 text-sm p-2 rounded-lg bg-secondary/30">
                    <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center border border-border shadow-sm">
                      <Edit3 className="w-4 h-4 text-primary" />
                    </div>
                    <div>
                      <div className="font-medium">Ghostwriter</div>
                      <div className="text-xs text-muted-foreground">Creator</div>
                    </div>
                  </div>
                  <div className="flex items-center gap-3 text-sm p-2 rounded-lg bg-secondary/30">
                    <div className="w-8 h-8 rounded-full bg-white flex items-center justify-center border border-border shadow-sm">
                      <CheckCircle className="w-4 h-4 text-primary" />
                    </div>
                    <div>
                      <div className="font-medium">Chief Editor</div>
                      <div className="text-xs text-muted-foreground">Reviewer</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Main Content Area */}
          <div className="lg:col-span-8 space-y-8">
            {/* Input Card */}
            <div className="bg-card rounded-xl border border-border p-1 shadow-sm">
              <div className="p-6 space-y-6">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-muted-foreground ml-1">Topic</label>
                  <input
                    type="text"
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    placeholder="What should we write about? (e.g., 'The Future of AI Agents')"
                    className="w-full px-4 py-4 bg-secondary/30 border-0 rounded-xl text-lg placeholder:text-muted-foreground/50 focus:ring-2 focus:ring-primary/20 focus:bg-white transition-all"
                    onKeyPress={(e) => e.key === 'Enter' && handleGenerate()}
                  />
                </div>

                <div className="flex flex-col sm:flex-row gap-4">
                  <div className="flex-1 space-y-2">
                    <label className="text-sm font-medium text-muted-foreground ml-1">Platform</label>
                    <div className="relative">
                      <select
                        value={platform}
                        onChange={(e) => setPlatform(e.target.value as 'twitter' | 'linkedin')}
                        className="w-full px-4 py-3 bg-secondary/30 border-0 rounded-xl appearance-none focus:ring-2 focus:ring-primary/20 focus:bg-white transition-all"
                      >
                        <option value="twitter">Twitter Thread</option>
                        <option value="linkedin">LinkedIn Post</option>
                      </select>
                      <ChevronDown className="absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground pointer-events-none" />
                    </div>
                  </div>

                  <div className="flex items-end">
                    <button
                      onClick={handleGenerate}
                      disabled={isGenerating}
                      className="w-full sm:w-auto px-8 py-3 bg-primary text-primary-foreground rounded-xl font-medium hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed transition-all flex items-center justify-center gap-2 shadow-sm"
                    >
                      {isGenerating ? (
                        <>
                          <Loader2 className="w-5 h-5 animate-spin" />
                          <span>Crafting...</span>
                        </>
                      ) : (
                        <>
                          <Sparkles className="w-5 h-5" />
                          <span>Generate Content</span>
                        </>
                      )}
                    </button>
                  </div>
                </div>
              </div>

              {error && (
                <div className="mx-6 mb-6 p-4 bg-red-50 text-red-600 text-sm rounded-lg border border-red-100 flex items-center gap-2">
                  <div className="w-1.5 h-1.5 rounded-full bg-red-500" />
                  {error}
                </div>
              )}
            </div>

            {/* Results Area */}
            {result && (
              <div className="space-y-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
                {/* Metrics Cards */}
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-card p-5 rounded-xl border border-border shadow-sm text-center">
                    <div className="text-3xl font-serif font-medium text-primary mb-1">
                      {result.virality_score}
                    </div>
                    <div className="text-xs text-muted-foreground uppercase tracking-wider font-medium">
                      Virality Score
                    </div>
                  </div>
                  <div className="bg-card p-5 rounded-xl border border-border shadow-sm text-center">
                    <div className="text-3xl font-serif font-medium text-primary mb-1">
                      {result.elapsed_time.toFixed(1)}s
                    </div>
                    <div className="text-xs text-muted-foreground uppercase tracking-wider font-medium">
                      Time
                    </div>
                  </div>
                  <div className="bg-card p-5 rounded-xl border border-border shadow-sm text-center">
                    <div className="text-3xl font-serif font-medium text-primary mb-1">
                      {result.iterations}
                    </div>
                    <div className="text-xs text-muted-foreground uppercase tracking-wider font-medium">
                      Iterations
                    </div>
                  </div>
                </div>

                {/* Content Tabs */}
                <div className="bg-card rounded-xl border border-border shadow-sm overflow-hidden">
                  <div className="flex border-b border-border bg-secondary/30">
                    <button
                      onClick={() => setActiveTab('content')}
                      className={`flex-1 py-4 text-sm font-medium transition-colors relative ${activeTab === 'content'
                          ? 'text-primary bg-card'
                          : 'text-muted-foreground hover:text-foreground hover:bg-secondary/50'
                        }`}
                    >
                      Ghostwriter
                      {activeTab === 'content' && (
                        <div className="absolute top-0 left-0 right-0 h-0.5 bg-primary" />
                      )}
                    </button>
                    <button
                      onClick={() => setActiveTab('research')}
                      className={`flex-1 py-4 text-sm font-medium transition-colors relative ${activeTab === 'research'
                          ? 'text-primary bg-card'
                          : 'text-muted-foreground hover:text-foreground hover:bg-secondary/50'
                        }`}
                    >
                      Trend Scout
                      {activeTab === 'research' && (
                        <div className="absolute top-0 left-0 right-0 h-0.5 bg-primary" />
                      )}
                    </button>
                    <button
                      onClick={() => setActiveTab('feedback')}
                      className={`flex-1 py-4 text-sm font-medium transition-colors relative ${activeTab === 'feedback'
                          ? 'text-primary bg-card'
                          : 'text-muted-foreground hover:text-foreground hover:bg-secondary/50'
                        }`}
                    >
                      Chief Editor
                      {activeTab === 'feedback' && (
                        <div className="absolute top-0 left-0 right-0 h-0.5 bg-primary" />
                      )}
                    </button>
                  </div>

                  <div className="p-6 lg:p-8">
                    {/* Content Tab */}
                    {activeTab === 'content' && (
                      <div className="space-y-8">
                        <div>
                          <div className="flex justify-between items-center mb-6">
                            <h3 className="font-serif text-xl font-medium">Final Draft</h3>
                            <button
                              onClick={downloadContent}
                              className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-primary hover:bg-secondary rounded-lg transition-colors"
                            >
                              <Download className="w-4 h-4" />
                              Export
                            </button>
                          </div>
                          <div className="prose prose-stone max-w-none prose-headings:font-serif prose-p:leading-relaxed bg-white p-8 rounded-lg border border-border shadow-sm">
                            <ReactMarkdown>{result.final_content}</ReactMarkdown>
                          </div>
                        </div>

                        {result.drafts.length > 0 && (
                          <div className="pt-8 border-t border-border">
                            <h3 className="font-serif text-lg font-medium mb-4 text-muted-foreground">Draft History</h3>
                            <div className="space-y-3">
                              {result.drafts.map((draft, index) => (
                                <details key={index} className="group border border-border rounded-lg bg-secondary/10 open:bg-white open:shadow-sm transition-all">
                                  <summary className="flex items-center justify-between p-4 cursor-pointer font-medium select-none">
                                    <div className="flex items-center gap-3">
                                      <span className="w-6 h-6 rounded-full bg-secondary flex items-center justify-center text-xs text-muted-foreground">
                                        {index + 1}
                                      </span>
                                      <span>Draft Version {index + 1}</span>
                                    </div>
                                    <div className="flex items-center gap-4">
                                      {result.scores[index] && (
                                        <span className={`text-sm px-2 py-1 rounded-md ${result.scores[index] >= settings.viralityThreshold
                                            ? 'bg-green-100 text-green-700'
                                            : 'bg-yellow-100 text-yellow-700'
                                          }`}>
                                          Score: {result.scores[index]}
                                        </span>
                                      )}
                                      <ChevronRight className="w-4 h-4 text-muted-foreground group-open:rotate-90 transition-transform" />
                                    </div>
                                  </summary>
                                  <div className="p-6 pt-0 border-t border-transparent group-open:border-border">
                                    <div className="prose prose-sm max-w-none prose-stone mt-4">
                                      <ReactMarkdown>{draft}</ReactMarkdown>
                                    </div>
                                  </div>
                                </details>
                              ))}
                            </div>
                          </div>
                        )}
                      </div>
                    )}

                    {/* Research Tab */}
                    {activeTab === 'research' && (
                      <div className="space-y-6">
                        <div className="flex items-center gap-2 mb-6">
                          <TrendingUp className="w-5 h-5 text-primary" />
                          <h3 className="font-serif text-xl font-medium">Research Angles</h3>
                        </div>
                        <div className="grid gap-6">
                          {result.research_angles.map((angle, index) => (
                            <div key={index} className="bg-white p-6 rounded-xl border border-border shadow-sm hover:shadow-md transition-shadow">
                              <h4 className="font-serif text-lg font-medium mb-3 text-primary">
                                {angle.title}
                              </h4>
                              <div className="space-y-4 text-sm leading-relaxed">
                                <div>
                                  <span className="font-medium text-foreground block mb-1">Why it works:</span>
                                  <p className="text-muted-foreground">{angle.why_viral}</p>
                                </div>
                                <div>
                                  <span className="font-medium text-foreground block mb-1">Summary:</span>
                                  <p className="text-muted-foreground">{angle.summary}</p>
                                </div>
                                {angle.sources.length > 0 && (
                                  <div className="pt-3 border-t border-border mt-3">
                                    <span className="text-xs font-medium text-muted-foreground uppercase tracking-wider block mb-2">Sources</span>
                                    <ul className="space-y-1">
                                      {angle.sources.map((source, i) => (
                                        <li key={i}>
                                          <a
                                            href={source}
                                            target="_blank"
                                            rel="noopener noreferrer"
                                            className="text-primary hover:underline truncate block"
                                          >
                                            {source}
                                          </a>
                                        </li>
                                      ))}
                                    </ul>
                                  </div>
                                )}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Feedback Tab */}
                    {activeTab === 'feedback' && (
                      <div className="space-y-6">
                        <div className="flex items-center gap-2 mb-6">
                          <CheckCircle className="w-5 h-5 text-primary" />
                          <h3 className="font-serif text-xl font-medium">Editorial Feedback</h3>
                        </div>
                        <div className="space-y-4">
                          {result.feedbacks.map((feedback, index) => {
                            const score = result.scores[index] || 0;
                            const isPassing = score >= settings.viralityThreshold;
                            return (
                              <div
                                key={index}
                                className={`p-6 rounded-xl border ${isPassing
                                    ? 'bg-green-50/50 border-green-100'
                                    : 'bg-amber-50/50 border-amber-100'
                                  }`}
                              >
                                <div className="flex items-center justify-between mb-3">
                                  <h4 className="font-medium flex items-center gap-2">
                                    <span>Review Round {index + 1}</span>
                                    {isPassing ? (
                                      <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full">Approved</span>
                                    ) : (
                                      <span className="text-xs bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full">Revision Needed</span>
                                    )}
                                  </h4>
                                  <span className="font-mono text-lg font-medium">
                                    {score}/100
                                  </span>
                                </div>
                                <p className="text-sm leading-relaxed whitespace-pre-wrap text-foreground/80">
                                  {feedback}
                                </p>
                              </div>
                            );
                          })}
                          {result.virality_score >= settings.viralityThreshold && (
                            <div className="p-4 bg-primary/5 border border-primary/10 rounded-xl flex items-start gap-3">
                              <Sparkles className="w-5 h-5 text-primary mt-0.5" />
                              <div>
                                <div className="font-medium text-primary mb-1">Final Polish Applied</div>
                                <p className="text-sm text-muted-foreground">
                                  The Chief Editor has applied a final layer of polish to ensure maximum engagement based on the approved draft.
                                </p>
                              </div>
                            </div>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
