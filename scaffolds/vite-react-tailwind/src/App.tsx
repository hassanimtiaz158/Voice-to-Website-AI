import React from "react";
import siteData from "../data/site.json";
import { MessageCircle, ShieldCheck, Truck, Phone, Mail, MapPin } from "lucide-react";

export default function App() {
  const { business, hero, features, contact, navigation } = siteData;

  const getIcon = (iconName: string) => {
    switch (iconName) {
      case "ShieldCheck":
        return <ShieldCheck className="w-8 h-8 text-amber-500" />;
      case "Truck":
        return <Truck className="w-8 h-8 text-amber-500" />;
      case "MessageCircle":
        return <MessageCircle className="w-8 h-8 text-amber-500" />;
      default:
        return <ShieldCheck className="w-8 h-8 text-amber-500" />;
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-white text-slate-800">
      {/* Navigation Header */}
      <header className="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-slate-100 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <span className="text-xl font-bold text-blue-900 tracking-tight">{business.name}</span>
          </div>
          <nav className="hidden md:flex space-x-8">
            {navigation.map((item, idx) => (
              <a
                key={idx}
                href={item.target}
                className="text-sm font-medium text-slate-600 hover:text-blue-900 transition-colors"
              >
                {item.label}
              </a>
            ))}
          </nav>
          <a
            href={`https://wa.me/${contact.phone.replace(/[^0-9]/g, "")}`}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-semibold px-4 py-2 rounded-full transition-colors shadow-sm"
          >
            <MessageCircle className="w-4 h-4" />
            <span>WhatsApp Us</span>
          </a>
        </div>
      </header>

      {/* Hero Section */}
      <section id="hero" className="relative py-20 lg:py-32 bg-gradient-to-b from-blue-50/60 to-white">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 text-center">
          <span className="inline-block px-3 py-1 text-xs font-semibold uppercase tracking-wider text-blue-800 bg-blue-100 rounded-full mb-4">
            {business.type}
          </span>
          <h1 className="text-4xl sm:text-6xl font-extrabold text-slate-900 tracking-tight leading-tight mb-6">
            {hero.headline}
          </h1>
          <p className="text-lg sm:text-xl text-slate-600 max-w-3xl mx-auto mb-10 leading-relaxed">
            {hero.subheadline}
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <a
              href="#features"
              className="w-full sm:w-auto px-8 py-3.5 bg-blue-900 hover:bg-blue-800 text-white font-semibold rounded-lg shadow-md transition-all text-center"
            >
              {hero.ctaText}
            </a>
            <a
              href={`https://wa.me/${contact.phone.replace(/[^0-9]/g, "")}`}
              target="_blank"
              rel="noopener noreferrer"
              className="w-full sm:w-auto px-8 py-3.5 bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold rounded-lg transition-all text-center"
            >
              {hero.secondaryCtaText}
            </a>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-slate-50 border-t border-slate-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="text-3xl font-bold text-slate-900 mb-4">Why Choose Us</h2>
            <p className="text-slate-600">Built on values of exceptional quality, honesty, and enduring craftsmanship.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feat, idx) => (
              <div
                key={idx}
                className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow"
              >
                <div className="mb-4">{getIcon(feat.icon)}</div>
                <h3 className="text-xl font-semibold text-slate-900 mb-2">{feat.title}</h3>
                <p className="text-slate-600 text-sm leading-relaxed">{feat.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-16 bg-white border-t border-slate-100">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 text-center">
          <h2 className="text-2xl font-bold text-slate-900 mb-8">Get In Touch</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
            <div className="flex items-start gap-3 p-4 rounded-lg bg-slate-50">
              <Phone className="w-5 h-5 text-blue-900 mt-0.5" />
              <div>
                <p className="text-xs text-slate-500 font-medium">Call / WhatsApp</p>
                <p className="text-sm font-semibold text-slate-900">{contact.phone}</p>
              </div>
            </div>
            <div className="flex items-start gap-3 p-4 rounded-lg bg-slate-50">
              <Mail className="w-5 h-5 text-blue-900 mt-0.5" />
              <div>
                <p className="text-xs text-slate-500 font-medium">Email</p>
                <p className="text-sm font-semibold text-slate-900">{contact.email}</p>
              </div>
            </div>
            <div className="flex items-start gap-3 p-4 rounded-lg bg-slate-50">
              <MapPin className="w-5 h-5 text-blue-900 mt-0.5" />
              <div>
                <p className="text-xs text-slate-500 font-medium">Visit Us</p>
                <p className="text-sm font-semibold text-slate-900">{contact.address}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto py-8 bg-slate-900 text-slate-400 border-t border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center text-xs">
          <p>© {new Date().getFullYear()} {business.name}. All rights reserved.</p>
          <p className="mt-1 text-slate-500">Autonomous website created via Voice-to-Website AI.</p>
        </div>
      </footer>
    </div>
  );
}
